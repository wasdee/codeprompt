---
title: Code Prompt
description: Code Prompt with context files injection

instruction_prompt: "Find the file that contains the "Hello, World!" message and return its file path."
---
The following text is a Git repository with code. The structure of the text is sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the repository ends when the symbols --END-- are encountered. Any further text beyond --END-- is meant to be interpreted as instructions using the aforementioned code as context.
----
src/main.ts
import { App } from "./app";

const app = new App();
app.start();

----
src/app.ts
export class App {
  start() {
    console.log("Hello, World!");
  }
}
--END--
{{ instruction_prompt }}
