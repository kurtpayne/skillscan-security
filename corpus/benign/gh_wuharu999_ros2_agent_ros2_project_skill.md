---
name: "ros2-project-skill"
description: "Entry skill for a ROS 2 robotic arm project. Routes requests to process, pattern, and project reference files with project-aware guidance."
version: "2.0.0"
status: "active"
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: wuharu999/ros2-agent-skills
# corpus-url: https://github.com/wuharu999/ros2-agent-skills/blob/4f2f37660eca061060360008b3c2b6ba464361da/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# ROS 2 Project Skill

## Purpose

This is the entry point for ROS 2 robotic arm work.

Use this skill to route a request to the right combination of:

- `processes/*.md` for response workflow
- `patterns/*.md` for file-type or subsystem guidance
- `project/*.md` for package ownership and architecture context

This file is intentionally lightweight. It should stay focused on routing, not on detailed ROS 2 implementation rules.

---

## Directory Contract

Use this skill directory as a modular reference set:

- `processes/`
  - workflow for teaching, debugging, and implementation
- `patterns/`
  - file-type and subsystem guidance
- `project/`
  - package boundaries, structure, and architecture

Current references:

- `processes/teach.md`
- `processes/debug.md`
- `processes/implement.md`
- `patterns/gazebo.md`
- `patterns/launch.md`
- `patterns/setup_py.md`
- `patterns/urdf.md`
- `patterns/cmake.md`
- `patterns/ros2_control.md`
- `patterns/moveit.md`
- `project/structure.md`
- `project/package_map.md`

---

## Routing Model

For each request, classify three things in this order:

1. Primary intent
   - teach
   - debug
   - implement

2. Technical target
   - launch
   - setup.py
   - urdf or xacro
   - cmake
   - ros2_control
   - moveit
   - project structure
   - package ownership

3. Scope
   - single file
   - single package
   - cross-package subsystem
   - project-wide architecture

Then open the smallest set of files that covers the task:

1. the relevant process file
2. the exact pattern file if there is one
3. a project file if package ownership or architecture matters

---

## Process Routing

Open exactly one primary process file first:

- `processes/teach.md`
  - use for explanation, walkthroughs, reviews, and concept teaching
  - common triggers:
    - "teach me"
    - "explain"
    - "what does this do"
    - "help me understand"

- `processes/debug.md`
  - use for failures, regressions, launch problems, build issues, missing topics, bad TF, controller problems, or runtime errors
  - common triggers:
    - "debug"
    - "why is this failing"
    - "error"
    - "not working"
    - "doesn't launch"

- `processes/implement.md`
  - use for adding, modifying, integrating, or extending behavior
  - common triggers:
    - "add"
    - "implement"
    - "create"
    - "write"
    - "integrate"
    - "refactor"

---

## Pattern Routing

Use the most specific pattern files that match the request:

- `patterns/gazebo.md`
  - Gazebo simulation launch, entity spawning, simulator bridges, simulated sensors, and simulation-specific startup wiring

- `patterns/launch.md`
  - ROS 2 launch files, bringup, parameters, included launches, RViz or controller startup

- `patterns/setup_py.md`
  - Python package installation, console scripts, resource installation, launch or config file installation

- `patterns/urdf.md`
  - URDF, Xacro, links, joints, frames, meshes, inertials, robot description integration

- `patterns/cmake.md`
  - `CMakeLists.txt`, C++ nodes, libraries, install rules, ament dependencies

- `patterns/ros2_control.md`
  - hardware interfaces, `ros2_control` XML, controller YAML, controller manager integration

- `patterns/moveit.md`
  - MoveIt configuration, planning groups, controllers, planning pipeline, motion planning bringup

Use multiple pattern files when the change crosses subsystem boundaries.

Example:

- "Add a new Python hardware monitor and launch it"
  - `processes/implement.md`
  - `patterns/setup_py.md`
  - `patterns/launch.md`

- "Spawn the arm in Gazebo with controllers and simulated sensors"
  - `processes/implement.md`
  - `patterns/gazebo.md`
  - `patterns/launch.md`
  - `patterns/ros2_control.md`

- "Debug why the trajectory controller does not activate"
  - `processes/debug.md`
  - `patterns/ros2_control.md`
  - `project/package_map.md`

---

## Project Routing

Use project references when the request is about where code belongs, which package owns a file, or how packages relate:

- `project/structure.md`
  - use for folder layout, package split, and architecture decisions

- `project/package_map.md`
  - use for package responsibilities, dependency direction, and cross-package change planning

If a request could change more than one package, open one of these project files.

---

## Response Rules

When using this skill:

- keep answers anchored to the user's robot project, not generic ROS 2 trivia
- name the exact files and packages involved
- prefer the smallest coherent set of edits
- explain cross-file relationships before changing multiple files
- use current ROS 2 best practices in examples
- verify behavior after edits when commands or tests are available

Process files define how to approach the task.
Pattern and project files define what structure and constraints to follow.

---

## Scaling Rules

This structure is designed to grow cleanly.

When adding a new pattern such as `patterns/gazebo.md`:

1. create the new file in `patterns/`
2. add one routing bullet in this `SKILL.md`
3. describe when it should be opened
4. reference related pattern and project files
5. keep detailed rules inside the new file, not here

Do the same for new project references.

If a topic becomes broad enough to require its own workflow, add a new `processes/*.md` file and update the process routing section.

---

## Selection Priority

When several references seem relevant, use this order:

1. primary process file
2. exact technical pattern file
3. secondary pattern file if the task spans multiple subsystems
4. project reference if ownership or architecture is part of the decision

Avoid opening unrelated references "just in case".

---

## Output Style

Aim for output that is:

- project-aware
- concrete
- minimal but complete
- explicit about file ownership
- structured around verification, not guesswork

When teaching, connect the file to runtime behavior.
When debugging, isolate the smallest reproducible symptom.
When implementing, cover every affected file required for a working change.