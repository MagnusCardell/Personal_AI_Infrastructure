#!/usr/bin/env bun

import { join } from "path";

const paiDir = process.env.PAI_DIR || join(process.env.HOME || "", ".claude");

console.log(paiDir);
