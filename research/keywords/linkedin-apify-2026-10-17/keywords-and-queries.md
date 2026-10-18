# Keywords and three-layer queries

Date: 2026-10-17
Status: working list for the Apify round. Query version 1 is not frozen. No run has been started.
Shape of every query: domain or tool, AND AI, AND skill. At most five `AND` / `OR` operators.

## Domain and tools

- architect
- architecture
- architectural
- BIM
- Revit
- Rhino
- Grasshopper
- Parametric
- "generative design"
- Rendering

## AI

- AI
- GenAI
- "generative AI"
- "artificial intelligence"
- Midjourney
- ChatGPT
- Copilot

## Skills — direct

- skill
- skills
- upskilling
- deskilling
- reskilling

## Skills — cognition and design

- creativity
- "critical thinking"
- judgment
- intuition
- authorship

## Skills — process and work

- workflow
- automation
- replace

## Queries — direct skill

1. `(architect OR architectural) AND (GenAI OR "generative AI") AND (skill OR skills)`
2. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND (skill OR skills)`
3. `(BIM OR Revit) AND (GenAI OR "generative AI") AND (skill OR skills)`
4. `(BIM OR Revit) AND (Midjourney OR ChatGPT) AND (skill OR skills)`
5. `(architect OR architectural) AND (GenAI OR "generative AI") AND (upskilling OR reskilling)`
6. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND (upskilling OR reskilling)`
7. `(Rhino OR Grasshopper) AND (GenAI OR "generative AI") AND (upskilling OR reskilling)`
8. `(Rhino OR Grasshopper) AND (Midjourney OR ChatGPT) AND (upskilling OR reskilling)`
9. `(architect OR architectural) AND (GenAI OR "generative AI") AND (deskilling OR reskilling)`
10. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND (deskilling OR reskilling)`
11. `(Parametric OR "generative design") AND (GenAI OR "generative AI") AND (deskilling OR reskilling)`
12. `(Parametric OR "generative design") AND (Midjourney OR ChatGPT) AND (deskilling OR reskilling)`
13. `(architect OR architectural) AND (AI OR "artificial intelligence") AND (skill OR skills)`
14. `(Rhino OR Grasshopper) AND Copilot AND (skill OR skills)`

## Queries — cognition and design

15. `(architect OR architectural) AND (GenAI OR "generative AI") AND (creativity OR judgment)`
16. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND (creativity OR judgment)`
17. `(Rendering OR architecture) AND (GenAI OR "generative AI") AND (creativity OR judgment)`
18. `(Rendering OR architecture) AND (Midjourney OR ChatGPT) AND (creativity OR judgment)`
19. `(architect OR architectural) AND (GenAI OR "generative AI") AND ("critical thinking" OR intuition)`
20. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND ("critical thinking" OR intuition)`
21. `(BIM OR Revit) AND (GenAI OR "generative AI") AND ("critical thinking" OR intuition)`
22. `(BIM OR Revit) AND (Midjourney OR ChatGPT) AND ("critical thinking" OR intuition)`
23. `(architect OR architectural) AND (GenAI OR "generative AI") AND (authorship OR judgment)`
24. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND (authorship OR judgment)`
25. `(Rhino OR Grasshopper) AND (GenAI OR "generative AI") AND (authorship OR judgment)`
26. `(Rhino OR Grasshopper) AND (Midjourney OR ChatGPT) AND (authorship OR judgment)`

## Queries — process and work

27. `(architect OR architectural) AND (GenAI OR "generative AI") AND (workflow OR automation)`
28. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND (workflow OR automation)`
29. `(Parametric OR "generative design") AND (GenAI OR "generative AI") AND (workflow OR automation)`
30. `(Parametric OR "generative design") AND (Midjourney OR ChatGPT) AND (workflow OR automation)`
31. `(architect OR architectural) AND (GenAI OR "generative AI") AND (replace OR automation)`
32. `(architect OR architectural) AND (Midjourney OR ChatGPT) AND (replace OR automation)`
33. `(Rendering OR architecture) AND (GenAI OR "generative AI") AND (replace OR automation)`
34. `(Rendering OR architecture) AND (Midjourney OR ChatGPT) AND (replace OR automation)`
35. `(BIM OR Revit) AND (AI OR "artificial intelligence") AND (workflow OR automation)`
36. `(BIM OR Revit) AND (Copilot OR ChatGPT) AND (workflow OR automation)`

## Apify searchQueries

```json
[
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (skill OR skills)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (skill OR skills)",
  "(BIM OR Revit) AND (GenAI OR \"generative AI\") AND (skill OR skills)",
  "(BIM OR Revit) AND (Midjourney OR ChatGPT) AND (skill OR skills)",
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (upskilling OR reskilling)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (upskilling OR reskilling)",
  "(Rhino OR Grasshopper) AND (GenAI OR \"generative AI\") AND (upskilling OR reskilling)",
  "(Rhino OR Grasshopper) AND (Midjourney OR ChatGPT) AND (upskilling OR reskilling)",
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (deskilling OR reskilling)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (deskilling OR reskilling)",
  "(Parametric OR \"generative design\") AND (GenAI OR \"generative AI\") AND (deskilling OR reskilling)",
  "(Parametric OR \"generative design\") AND (Midjourney OR ChatGPT) AND (deskilling OR reskilling)",
  "(architect OR architectural) AND (AI OR \"artificial intelligence\") AND (skill OR skills)",
  "(Rhino OR Grasshopper) AND Copilot AND (skill OR skills)",
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (creativity OR judgment)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (creativity OR judgment)",
  "(Rendering OR architecture) AND (GenAI OR \"generative AI\") AND (creativity OR judgment)",
  "(Rendering OR architecture) AND (Midjourney OR ChatGPT) AND (creativity OR judgment)",
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (\"critical thinking\" OR intuition)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (\"critical thinking\" OR intuition)",
  "(BIM OR Revit) AND (GenAI OR \"generative AI\") AND (\"critical thinking\" OR intuition)",
  "(BIM OR Revit) AND (Midjourney OR ChatGPT) AND (\"critical thinking\" OR intuition)",
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (authorship OR judgment)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (authorship OR judgment)",
  "(Rhino OR Grasshopper) AND (GenAI OR \"generative AI\") AND (authorship OR judgment)",
  "(Rhino OR Grasshopper) AND (Midjourney OR ChatGPT) AND (authorship OR judgment)",
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (workflow OR automation)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (workflow OR automation)",
  "(Parametric OR \"generative design\") AND (GenAI OR \"generative AI\") AND (workflow OR automation)",
  "(Parametric OR \"generative design\") AND (Midjourney OR ChatGPT) AND (workflow OR automation)",
  "(architect OR architectural) AND (GenAI OR \"generative AI\") AND (replace OR automation)",
  "(architect OR architectural) AND (Midjourney OR ChatGPT) AND (replace OR automation)",
  "(Rendering OR architecture) AND (GenAI OR \"generative AI\") AND (replace OR automation)",
  "(Rendering OR architecture) AND (Midjourney OR ChatGPT) AND (replace OR automation)",
  "(BIM OR Revit) AND (AI OR \"artificial intelligence\") AND (workflow OR automation)",
  "(BIM OR Revit) AND (Copilot OR ChatGPT) AND (workflow OR automation)"
]
```
