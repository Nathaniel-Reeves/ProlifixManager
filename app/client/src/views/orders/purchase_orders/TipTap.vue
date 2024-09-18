<template>
  <b-card v-if="editor" class="container" style="box-shadow: 0 2px 2px rgba(0,0,0,.2);">
    <div class="mb-3">
      <b-button-group>
        <!-- BlockQuote Menu -->
        <b-button title="Blockquote Left" v-b-tooltip.hover variant="light" @click="editor.chain().focus().setBlockquote().run()" :disabled="!editor.can().setBlockquote()">
          <b-icon icon="blockquote-left" />
        </b-button>
        <b-button title="Blockquote Right" v-b-tooltip.hover variant="light" @click="editor.chain().focus().unsetBlockquote().run()" :disabled="!editor.can().unsetBlockquote()">
          <b-icon icon="blockquote-right" />
        </b-button>
      </b-button-group>
      <!-- List Menu -->
      <b-button-group>
        <b-button title="Unordered List" v-b-tooltip.hover variant="light" @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
          <b-icon icon="list-ul" />
        </b-button>
      </b-button-group>
      <!-- Image Menu -->
      <b-button-group>
        <b-button title="Upload Image" v-b-tooltip.hover variant="light" @click="addImage">
          <b-icon icon="image" />
        </b-button>
      </b-button-group>
      <!-- Align Group -->
       <b-button-group>
        <b-button title="Left Align" v-b-tooltip.hover variant="light" @click="editor.chain().focus().setTextAlign('left').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }">
          <b-icon icon="text-left" />
        </b-button>
        <b-button title="Center Align" v-b-tooltip.hover variant="light" @click="editor.chain().focus().setTextAlign('center').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }">
          <b-icon icon="text-center" />
        </b-button>
        <b-button title="Right Align" v-b-tooltip.hover variant="light" @click="editor.chain().focus().setTextAlign('right').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }">
          <b-icon icon="text-right" />
        </b-button>
      </b-button-group>
      <!-- Undo-Redo Group -->
       <b-button-group>
        <b-button title="Undo" v-b-tooltip.hover variant="light" @click="editor.chain().focus().undo().run()" :disabled="!editor.can().undo()">
          <b-icon icon="arrow90deg-left" />
        </b-button>
        <b-button title="Redo" v-b-tooltip.hover variant="light" @click="editor.chain().focus().redo().run()" :disabled="!editor.can().redo()">
          <b-icon icon="arrow90deg-right" />
        </b-button>
       </b-button-group>
       <!-- Font Family Group -->
       <button @click="editor.chain().focus().setFontFamily('Inter').run()">
          Inter
        </button>
        <button @click="editor.chain().focus().setFontFamily('Comic Sans MS, Comic Sans').run()">
          Comic Sans
        </button>
        <button @click="editor.chain().focus().setFontFamily('serif').run()">
          Serif
        </button>
        <button @click="editor.chain().focus().setFontFamily('monospace').run()">
          Monospace
        </button>
        <button @click="editor.chain().focus().setFontFamily('cursive').run()">
          Cursive
        </button>
        <button @click="editor.chain().focus().unsetFontFamily().run()">
          Unset font family
        </button>
    </div>
    <hr>
    <editor-content :editor="editor" />
  </b-card>
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-3'
import Blockquote from '@tiptap/extension-blockquote'
import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import BulletList from '@tiptap/extension-bullet-list'
import ListItem from '@tiptap/extension-list-item'
import Dropcursor from '@tiptap/extension-dropcursor'
import Image from '@tiptap/extension-image'
import TextAlign from '@tiptap/extension-text-align'
import Heading from '@tiptap/extension-heading'
import Typography from '@tiptap/extension-typography'
import History from '@tiptap/extension-history'
import Placeholder from '@tiptap/extension-placeholder'
import ListKeymap from '@tiptap/extension-list-keymap'
import Gapcursor from '@tiptap/extension-gapcursor'
import FontFamily from '@tiptap/extension-font-family'

export default {
  components: {
    EditorContent
  },
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      editor: null
    }
  },
  watch: {
    value (value) {
      // HTML
      const isSame = this.editor.getHTML() === value

      // JSON
      // const isSame = JSON.stringify(this.editor.getJSON()) === JSON.stringify(value)

      if (isSame) {
        return
      }

      this.editor.commands.setContent(value, false)
    }
  },
  methods: {
    addImage () {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = 'image/*'

      input.addEventListener('change', (event) => {
        const file = event.target.files[0]

        if (file) {
          const reader = new FileReader()
          reader.onload = (e) => {
            const url = e.target.result
            console.log('Image URL:', url)
            this.editor.chain().focus().setImage({ src: url }).run()
          }

          reader.readAsDataURL(file)
        }
      })

      input.click()
    }
  },
  mounted () {
    this.editor = new Editor({
      content: this.value,
      extensions: [
        Document,
        Paragraph,
        Text,
        Blockquote,
        BulletList,
        ListItem,
        Dropcursor,
        Image.configure({
          allowBase64: true,
          inline: true
        }),
        Heading,
        TextAlign.configure({
          types: ['heading', 'paragraph'],
          default: 'right'
        }),
        Typography,
        History,
        Placeholder.configure({
          // Use a placeholder:
          // placeholder: 'Write something …',
          // Use different placeholders depending on the node type:
          placeholder: ({ node }) => {
            if (node.type.name === 'heading') {
              return 'What’s the title?'
            }

            return 'Write here ...'
          },
          showOnlyWhenEditable: true
        }),
        ListKeymap,
        Gapcursor,
        FontFamily
      ],
      onUpdate: () => {
        // HTML
        this.$emit('input', this.editor.getHTML())

        // JSON
        // this.$emit('input', this.editor.getJSON())
      }
    })
  },

  beforeDestroy () {
    this.editor.destroy()
  }
}
</script>

<style lang="scss">

/* Basic editor styles */
.tiptap {
  :first-child {
    margin-top: 0;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
    margin-top: 2.5rem;
    text-wrap: pretty;
  }

  h1,
  h2 {
    margin-top: 3.5rem;
    margin-bottom: 1.5rem;
  }

  h1 {
    font-size: 1.4rem;
  }

  h2 {
    font-size: 1.2rem;
  }

  h3 {
    font-size: 1.1rem;
  }

  h4,
  h5,
  h6 {
    font-size: 1rem;
  }

  blockquote {
    border-left: 3px solid var(--gray-3);
    margin: 1.5rem 0;
    padding-left: 1rem;
  }

  code {
    background-color: var(--purple-light);
    border-radius: 0.4rem;
    color: var(--black);
    font-size: 0.85rem;
    padding: 0.25em 0.3em;
  }

  pre {
    background: var(--black);
    border-radius: 0.5rem;
    color: var(--white);
    font-family: 'JetBrainsMono', monospace;
    margin: 1.5rem 0;
    padding: 0.75rem 1rem;

    code {
      background: none;
      color: inherit;
      font-size: 0.8rem;
      padding: 0;
    }
  }

  hr {
    border: none;
    border-top: 1px solid var(--gray-2);
    margin: 2rem 0;
  }

  /* Placeholder (at the top) */
  p.is-editor-empty:first-child::before {
    color: var(--gray-4);
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;
  }

  img {
    display: block;
    height: auto;
    margin: 1.5rem 0;
    max-width: 100%;

    &.ProseMirror-selectednode {
      outline: 3px solid var(--purple);
    }
  }
}
</style>
