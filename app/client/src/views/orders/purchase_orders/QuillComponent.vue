<template>
  <div>
    <b-button @click="toggleEdit()">Toggle Edit</b-button>
    <div>
      <div v-show="edit" class="my-3">
        <div ref="editor"></div>
      </div>
      <div v-show="!edit" class="my-3">
        <div ref="viewer"></div>
      </div>
    </div>

    <link href="https://unpkg.com/quill-table-ui@1.0.5/dist/index.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.bubble.css" rel="stylesheet" />
  </div>
</template>

<script>
import Quill from 'quill'
import Delta from 'quill-delta'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import BlotFormatter from 'quill-blot-formatter'
import * as QuillTableUI from 'quill-table-ui'
import ImageCompress from 'quill-image-compress'
import katex from 'katex' // for formula button
import 'katex/dist/katex.min.css'

Quill.register('modules/blotFormatter', BlotFormatter)
Quill.register({
  'modules/tableUI': QuillTableUI.default
}, true)
Quill.register('modules/imageCompress', ImageCompress)

export default {
  name: 'QuillComponent',
  data: function () {
    return {
      editor: null,
      viewer: null,
      edit: false,
      content: {}
    }
  },
  props: {
    modelValue: {
      default: new Delta()
    }
  },
  mounted: function () {
    window.katex = katex
    var _this = this

    // Build Editor
    this.editor = new Quill(this.$refs.editor, {
      theme: 'snow',
      placeholder: 'Type something in here!',
      modules: {
        blotFormatter: {},
        toolbar: [
          ['bold', 'italic', 'underline', 'strike'],
          ['blockquote', 'code-block'],
          ['link', 'image', 'video', 'formula', 'table'],
          [{ header: 4 }, { header: 5 }],
          [{ list: 'ordered' }, { list: 'bullet' }, { list: 'check' }],
          [{ script: 'sub' }, { script: 'super' }],
          [{ indent: '-1' }, { indent: '+1' }],
          [{ direction: 'rtl' }],
          [{ size: ['small', false, 'large', 'huge'] }],
          [{ color: [] }, { background: [] }],
          [{ font: [] }],
          [{ align: [] }],
          ['clean']
        ],
        table: true,
        tableUI: true,
        imageCompress: {
          quality: 0.9,
          maxWidth: 1000,
          maxHeight: 1000
        }
      }
    })

    this.editor.on('editor-change', function () {
      return _this.update()
    })

    // Build Viewer
    this.viewer = new Quill(this.$refs.viewer, {
      theme: 'bubble',
      placeholder: 'No Text Yet.',
      modules: {
        blotFormatter: {},
        toolbar: [
          ['bold', 'italic', 'underline', 'strike'],
          ['blockquote', 'code-block'],
          ['link', 'image', 'video', 'formula', 'table'],
          [{ header: 4 }, { header: 5 }],
          [{ list: 'ordered' }, { list: 'bullet' }, { list: 'check' }],
          [{ script: 'sub' }, { script: 'super' }],
          [{ indent: '-1' }, { indent: '+1' }],
          [{ direction: 'rtl' }],
          [{ size: ['small', false, 'large', 'huge'] }],
          [{ color: [] }, { background: [] }],
          [{ font: [] }],
          [{ align: [] }],
          ['clean']
        ],
        table: true,
        tableUI: true,
        imageCompress: {
          quality: 0.9,
          maxWidth: 1000,
          maxHeight: 1000
        }
      }
    })

    // Disable viewer from getting clicked by user
    this.$refs.viewer.style.pointerEvents = 'none'

    if (this.contents) {
      this.editor.setContents(this.contents)
      this.viewer.setContents(this.contents)
    }
  },
  methods: {
    update: function () {
      this.content = this.editor.getContents()
    },
    toggleEdit: function () {
      if (this.edit) {
        this.viewer.setContents(this.content)
        this.$emit('update:modelValue', this.content)
      }
      this.edit = !this.edit
    }
  },
  created: function () {
    const delta = new Delta()
    this.content = delta

    // check if modelValue is valid delta
    if (this.modelValue && this.modelValue.ops) {
      this.content = this.modelValue
    }
  }
}
</script>
