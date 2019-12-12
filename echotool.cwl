#!/usr/bin/env cwl-runner

class: CommandLineTool
cwlVersion: v1.0
id: echo-tool
baseCommand: echo
inputs:
  message:
    type: string
    inputBinding:
      position: 1
outputs: []
