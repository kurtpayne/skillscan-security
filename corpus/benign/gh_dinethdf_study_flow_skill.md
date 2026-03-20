---
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: dinethdf/study-flow
# corpus-url: https://github.com/dinethdf/study-flow/blob/b8773aa6ba9f56af7beb294eb729988372373af6/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: plain_instructions
---
# SKILL.md — StudyFlow Custom Agent Skills

> This file defines how the agent handles specific, repeatable tasks in this project.
> Before implementing any of the scenarios below, read the relevant skill section completely.

---

## Skill 1 — Student Email Validation

**When to use:** Any form or API route where a student registers or updates their email.

### Rules
- Email must be a valid email format (use Zod `.email()`).
- For university students, email must end in `.edu`, `.ac.lk`, `.ac.uk`, `.ac.in`, or any known academic domain.
- For school students, email validation is standard (no domain restriction).
- Reject disposable/temporary email domains (e.g., mailinator.com, tempmail.com).

### Zod Schema Template
```typescript
import { z } from 'zod';

const ACADEMIC_DOMAINS = ['.edu', '.ac.lk', '.ac.uk', '.ac.in', '.edu.au', '.ac.nz'];
const DISPOSABLE_DOMAINS = ['mailinator.com', 'tempmail.com', 'throwaway.email'];

export const studentEmailSchema = z.string()
  .email({ message: 'Please enter a valid email address.' })
  .refine(
    (email) => !DISPOSABLE_DOMAINS.some(d => email.endsWith(d)),
    { message: 'Disposable email addresses are not allowed.' }
  );

export const universityEmailSchema = studentEmailSchema.refine(
  (email) => ACADEMIC_DOMAINS.some(domain => email.endsWith(domain)),
  { message: 'University students must use an academic email address (.edu, .ac.lk, etc.).' }
);
```

---

## Skill 2 — File Uploads to Supabase Storage

**When to use:** When a student uploads any file (profile photo, study material, etc.).

### Rules
- Max file size: **5MB**
- Allowed types: `image/jpeg`, `image/png`, `image/webp`, `application/pdf`
- File path format: `{userId}/{feature}/{timestamp}-{filename}`
- Always upload from a **server-side API route** — never directly from the client.
- Return the public URL after successful upload.

### Upload Service Template
```typescript
// /lib/services/StorageService.ts
import { createServerSupabaseClient } from '@/lib/supabase/server';

export class StorageService {
  private supabase;

  constructor(supabase: ReturnType<typeof createServerSupabaseClient>) {
    this.supabase = supabase; // Constructor injection
  }

  async uploadFile(
    userId: string,
    feature: string,
    file: File
  ): Promise<{ url: string; path: string }> {
    const MAX_SIZE = 5 * 1024 * 1024; // 5MB
    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];

    if (file.size > MAX_SIZE) throw new Error('File size exceeds 5MB limit.');
    if (!ALLOWED_TYPES.includes(file.type)) throw new Error('File type not allowed.');

    const timestamp = Date.now();
    const safeName = file.name.replace(/[^a-zA-Z0-9.-]/g, '_');
    const path = `${userId}/${feature}/${timestamp}-${safeName}`;

    const { error } = await this.supabase.storage
      .from('studyflow-uploads')
      .upload(path, file, { upsert: false });

    if (error) throw new Error(`Upload failed: ${error.message}`);

    const { data } = this.supabase.storage
      .from('studyflow-uploads')
      .getPublicUrl(path);

    return { url: data.publicUrl, path };
  }
}
```

---

## Skill 3 — Subject & Topic UI Component Template

**When to use:** When building or modifying any component related to subjects or topics.

### Rules
- Subject cards must show: subject name, color indicator, overall progress bar, topic count.
- Topic list items must show: topic name, individual progress percentage, completion checkbox.
- Progress bars use Tailwind's `bg-blue-500` for active, `bg-gray-200` for background.
- Completion percentage input is a slider (0–100) + a number input — both stay in sync.
- Use optimistic UI updates — update the UI immediately, sync to DB in background.

### Component Structure Template
```tsx
// /components/features/subjects/SubjectCard.tsx
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import type { SubjectWithTopics } from '@/types';

interface SubjectCardProps {
  subject: SubjectWithTopics;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

export function SubjectCard({ subject, onEdit, onDelete }: SubjectCardProps) {
  const avgProgress = subject.topics.length
    ? Math.round(subject.topics.reduce((sum, t) => sum + t.completionPct, 0) / subject.topics.length)
    : subject.completionPct;

  return (
    <div className="rounded-xl border border-border bg-card p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: subject.color }} />
          <h3 className="font-semibold text-sm">{subject.name}</h3>
        </div>
        <Badge variant="secondary">{subject.topics.length} topics</Badge>
      </div>
      <Progress value={avgProgress} className="h-2 mb-1" />
      <p className="text-xs text-muted-foreground">{avgProgress}% complete</p>
    </div>
  );
}
```

---

## Skill 4 — AI Schedule Generation

**When to use:** When the agent needs to call Gemini to generate a study schedule.

### Rules
- Never call Gemini from the client side — always use `/api/schedule/generate/route.ts`.
- Pass subjects, topics, completion percentages, and exam dates as structured JSON in the prompt.
- Always request JSON output from Gemini — parse and validate before saving.
- If Gemini fails, return a fallback rule-based schedule (do not throw an error to the user).
- Rate limit: max 1 schedule generation per user per 10 minutes.

### Prompt Template
```typescript
// /lib/ai/scheduleGenerator.ts
export function buildSchedulePrompt(data: ScheduleInput): string {
  return `
You are a study schedule expert. Generate a personalized daily study plan.

Student Data:
${JSON.stringify(data, null, 2)}

Rules:
- Prioritize subjects with low completion AND close exam dates.
- Max 3 subjects per day to avoid burnout.
- Each study session is 45–90 minutes.
- Leave weekends lighter (max 2 subjects).
- Days with exams should be light review only.

Return ONLY valid JSON in this exact format:
{
  "schedule": [
    {
      "date": "YYYY-MM-DD",
      "sessions": [
        {
          "subjectId": "string",
          "topicId": "string or null",
          "startTime": "HH:MM",
          "durationMinutes": 60,
          "sessionType": "new_material | review | exam_prep"
        }
      ]
    }
  ]
}
`;
}
```

---

## Skill 5 — API Route Template

**When to use:** Every time the agent creates a new API route.

### Standard Template
```typescript
// /app/api/[feature]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase/server';
import { z } from 'zod';

const inputSchema = z.object({
  // define fields here
});

export async function POST(req: NextRequest) {
  try {
    // 1. Auth check
    const supabase = createServerSupabaseClient();
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // 2. Parse & validate input
    const body = await req.json();
    const parsed = inputSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }

    // 3. Business logic (via service)
    // const result = await myService.doSomething(parsed.data);

    // 4. Return response
    return NextResponse.json({ data: null }, { status: 200 });

  } catch (error) {
    console.error('[API ERROR]', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```