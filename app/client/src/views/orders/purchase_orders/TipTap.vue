<template>
  <b-card v-if="editor" class="w-100" style="box-shadow: 0 2px 2px rgba(0,0,0,.2);">
    <div class="mb-3" v-show="edit">
      <!-- Text Style Menu -->
      <b-button-group class="ml-2">
        <b-button title="Bold" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleBold().run()" :class="{ 'is-active': editor.isActive('bold') }">
          <b-icon icon="type-bold" />
        </b-button>
        <b-button title="Italic" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleItalic().run()" :class="{ 'is-active': editor.isActive('italic') }">
          <b-icon icon="type-italic" />
        </b-button>
        <b-button title="Underline" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleUnderline().run()" :class="{ 'is-active': editor.isActive('underline') }">
          <b-icon icon="type-underline" />
        </b-button>
        <b-button title="Strike" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleStrike().run()" :class="{ 'is-active': editor.isActive('strike') }">
          <b-icon icon="type-strikethrough" />
        </b-button>
        <b-button title="Superscript" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleSuperscript().run()" :class="{ 'is-active': editor.isActive('superscript') }">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-superscript" viewBox="0 0 16 16">
            <path d="m4.266 12.496.96-2.853H8.76l.96 2.853H11L7.62 3H6.38L3 12.496zm2.748-8.063 1.419 4.23h-2.88l1.426-4.23zm5.132-1.797v-.075c0-.332.234-.618.619-.618.354 0 .618.256.618.58 0 .362-.271.649-.52.898l-1.788 1.832V6h3.59v-.958h-1.923v-.045l.973-1.04c.415-.438.867-.845.867-1.547 0-.8-.701-1.41-1.787-1.41C11.565 1 11 1.8 11 2.576v.06z"/>
          </svg>
        </b-button>
        <b-button title="Subscript" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleSubscript().run()" :class="{ 'is-active': editor.isActive('subscript') }">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-subscript" viewBox="0 0 16 16">
            <path d="m3.266 12.496.96-2.853H7.76l.96 2.853H10L6.62 3H5.38L2 12.496zm2.748-8.063 1.419 4.23h-2.88l1.426-4.23zm6.132 7.203v-.075c0-.332.234-.618.619-.618.354 0 .618.256.618.58 0 .362-.271.649-.52.898l-1.788 1.832V15h3.59v-.958h-1.923v-.045l.973-1.04c.415-.438.867-.845.867-1.547 0-.8-.701-1.41-1.787-1.41-1.23 0-1.795.8-1.795 1.576v.06z"/>
          </svg>
        </b-button>
        <!-- <b-button title="Code Block" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleCodeBlock().run()" :class="{ 'is-active': editor.isActive('codeBlock') }">
          <b-icon icon="code-slash" />
        </b-button> -->
      </b-button-group>
      <!-- BlockQuote Menu -->
      <b-button-group class="ml-2">
        <b-button title="Blockquote Left" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().setBlockquote().run()" :disabled="!editor.can().setBlockquote()">
          <b-icon icon="blockquote-left" />
        </b-button>
        <b-button title="Blockquote Right" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().unsetBlockquote().run()" :disabled="!editor.can().unsetBlockquote()">
          <b-icon icon="blockquote-right" />
        </b-button>
      </b-button-group>
      <!-- List Menu -->
      <b-button-group class="ml-2">
        <b-button title="Unordered List" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleBulletList().run()" :class="{ 'is-active': editor.isActive('bulletList') }">
          <b-icon icon="list-ul" />
        </b-button>
        <b-button title="Ordered List" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleOrderedList().run()" :class="{ 'is-active': editor.isActive('orderedList') }">
          <b-icon icon="list-ol" />
        </b-button>
      </b-button-group>
      <!-- Extra Content Menu -->
      <b-button-group class="ml-2">
        <b-button title="Upload Image" v-b-tooltip.hover variant="light" class="text-editor-button" @click="addImage">
          <b-icon icon="image" />
        </b-button>
        <button title="Embed Youtube Video" v-b-tooltip.hover variant="light" class="text-editor-button" @click="addVideo">
          <b-icon icon="youtube" />
        </button>
        <b-button title="Add Link" v-b-tooltip.hover variant="light" class="text-editor-button" v-if="!editor.isActive('link')" @click="setLink" :class="{ 'is-active': editor.isActive('link') }">
          <b-icon icon="link" />
        </b-button>
        <b-button title="Remove Link" v-b-tooltip.hover variant="light" class="text-editor-button" v-else @click="editor.chain().focus().unsetLink().run()" :class="{ 'is-active': editor.isActive('link') }">
          <b-icon icon="link" />
        </b-button>
      </b-button-group>
      <!-- Align Group -->
       <b-button-group class="ml-2">
        <b-button title="Left Align" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().setTextAlign('left').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }">
          <b-icon icon="text-left" />
        </b-button>
        <b-button title="Center Align" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().setTextAlign('center').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }">
          <b-icon icon="text-center" />
        </b-button>
        <b-button title="Right Align" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().setTextAlign('right').run()" :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }">
          <b-icon icon="text-right" />
        </b-button>
      </b-button-group>
      <!-- Undo-Redo Group -->
      <b-button-group class="ml-2">
        <b-button title="Undo" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().undo().run()" :disabled="!editor.can().undo()">
          <b-icon icon="arrow90deg-left" />
        </b-button>
        <b-button title="Redo" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().redo().run()" :disabled="!editor.can().redo()">
          <b-icon icon="arrow90deg-right" />
        </b-button>
      </b-button-group>
      <!-- Font Family Group -->
      <b-dropdown title="Select Font" v-b-tooltip.hover variant="light" no-caret toggle-class="text-editor-button" right text="Font" class="ml-2">
        <b-dropdown-item @click="editor.chain().focus().setFontFamily('Inter').run()">Inter</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().setFontFamily('serif').run()">Serif</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().setFontFamily('monospace').run()">Monospace</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().setFontFamily('cursive').run()">Cursive</b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item @click="editor.chain().focus().unsetFontFamily().run()">Default Font</b-dropdown-item>
      </b-dropdown>
      <!-- Heading Group -->
      <b-button-group class="ml-2">
        <b-button title="Heading 3" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }">
          H3
        </b-button>
        <b-button title="Heading 4" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleHeading({ level: 4 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 4 }) }">
          H4
        </b-button>
        <b-button title="Heading 5" v-b-tooltip.hover variant="light" class="text-editor-button" @click="editor.chain().focus().toggleHeading({ level: 5 }).run()" :class="{ 'is-active': editor.isActive('heading', { level: 5 }) }">
          H5
        </b-button>
      </b-button-group>
      <!-- Highlight Group -->
      <b-dropdown title="Highlighter" v-b-tooltip.hover variant="light" no-caret toggle-class="text-editor-button" :class="['text-editor-button', 'ml-2', { 'is-active': editor.isActive('highlight') }]">
        <template #button-content>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" color="#000000" fill="none">
            <path d="M15.2141 5.98239L16.6158 4.58063C17.39 3.80646 18.6452 3.80646 19.4194 4.58063C20.1935 5.3548 20.1935 6.60998 19.4194 7.38415L18.0176 8.78591M15.2141 5.98239L6.98023 14.2163C5.93493 15.2616 5.41226 15.7842 5.05637 16.4211C4.70047 17.058 4.3424 18.5619 4 20C5.43809 19.6576 6.94199 19.2995 7.57889 18.9436C8.21579 18.5877 8.73844 18.0651 9.78375 17.0198L18.0176 8.78591M15.2141 5.98239L18.0176 8.78591" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M11 20H17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </template>
        <b-dropdown-item @click="editor.chain().focus().toggleHighlight({ color: '#ffcc00' }).run()" :class="{ 'is-active': editor.isActive('highlight', { color: '#ffcc00' }) }">Yellow</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().toggleHighlight({ color: '#8ce99a' }).run()" :class="{ 'is-active': editor.isActive('highlight', { color: '#8ce99a' }) }">Green</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().toggleHighlight({ color: '#ffc078' }).run()" :class="{ 'is-active': editor.isActive('highlight', { color: '#ffc078' }) }">Orange</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().toggleHighlight({ color: '#b197fc' }).run()" :class="{ 'is-active': editor.isActive('highlight', { color: '#b197fc' }) }">Red</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().toggleHighlight({ color: '#b197fc' }).run()" :class="{ 'is-active': editor.isActive('highlight', { color: '#b197fc' }) }">Purple</b-dropdown-item>
        <b-dropdown-item @click="editor.chain().focus().toggleHighlight({ color: '#74c0fc' }).run()" :class="{ 'is-active': editor.isActive('highlight', { color: '#74c0fc' }) }">Blue</b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item @click="editor.chain().focus().unsetHighlight().run()" :disabled="!editor.isActive('highlight')">Remove Highlight</b-dropdown-item>
      </b-dropdown>
      <!-- Spell Check -->
      <b-dropdown title="Spell Check" v-b-tooltip.hover variant="light" no-caret toggle-class="text-editor-button" class="ml-2">
        <template #button-content>
          <!-- <b-icon icon="check2-square" /> -->
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 32 32">
            <path xmlns="http://www.w3.org/2000/svg" d="M20,22h2L17,10H15L10,22h2l1.24-3h5.53Zm-5.93-5,1.82-4.42h.25L18,17Z"/>
            <path xmlns="http://www.w3.org/2000/svg" d="M12,28H6a2,2,0,0,1-2-2V6A2,2,0,0,1,6,4H26a2,2,0,0,1,2,2V17H26V6H6V26h6Z"/>
            <polygon xmlns="http://www.w3.org/2000/svg" points="23 27.18 20.41 24.59 19 26 23 30 30 23 28.59 21.59 23 27.18"/>
          </svg>
        </template>
        <b-dropdown-item href="https://www.grammarly.com/browser/chrome" target="_blank">Use Grammarly</b-dropdown-item>
      </b-dropdown>
      <!-- Table Group -->
      <b-dropdown id="tablemenu" toggle-class="text-editor-button" variant="light" text="Table" class="ml-2">
        <template #button-content>
          <b-icon icon="table" />
        </template>
        <b-dropdown-header id="dropdown-header-label">
          Table Options
        </b-dropdown-header>
        <b-dropdown id="tablesizemenu" no-caret variant="light" text="New Table" toggle-class="stripped-dropdown" dropright style="width: 100%;">
          <template #button-content>
            <div class="d-flex justify-content-start">
              <b-icon icon="table" class="mr-2"/>
              <span>New Table</span>
            </div>
          </template>
          <b-dropdown-header id="dropdown-header-label">
            Table Size
          </b-dropdown-header>
          <b-dropdown-item>
            <div v-for="col in 10" :key="col" class="d-flex justify-content-between" v-align="center">
              <div v-for="row in 10" :key="row" class="d-flex justify-content-between" v-align="center">
                <b-icon icon="squre" class="mr-2"/>
              </div>
            </div>
          </b-dropdown-item>
        </b-dropdown>
        <b-dropdown-item-button class="d-flex justify-content-start" link-class="w-100 pl-1">
          <b-icon icon="table" class="mr-2"/>
          <span>Add Column</span>
        </b-dropdown-item-button>
        <b-dropdown-item-button class="d-flex justify-content-start" link-class="w-100 pl-1">
          <b-icon icon="table" class="mr-2"/>
          <span>Remove Column</span>
        </b-dropdown-item-button>
      </b-dropdown>
    </div>
    <hr v-show="edit">
    <editor-content :editor="editor"/>
    <div v-if="edit" class="d-flex justify-content-end">
      <div :class="{'character-count': true, 'character-count--warning': editor.storage.characterCount.characters() === limit}">
        <svg height="20" width="20" viewBox="0 0 20 20">
          <circle r="10" cx="10" cy="10" fill="#e9ecef"/>
          <circle r="5" cx="10" cy="10" fill="transparent" stroke="currentColor" stroke-width="10" :stroke-dasharray="`calc(${percentage} * 31.4 / 100) 31.4`" transform="rotate(-90) translate(-20)"/>
          <circle r="6" cx="10" cy="10" fill="white"/>
        </svg>
        {{ editor.storage.characterCount.characters() }} / {{ limit }} characters
        <br>
        {{ editor.storage.characterCount.words() }} words
      </div>
    </div>
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
import Typography from '@tiptap/extension-typography'
import History from '@tiptap/extension-history'
import Placeholder from '@tiptap/extension-placeholder'
import ListKeymap from '@tiptap/extension-list-keymap'
import Gapcursor from '@tiptap/extension-gapcursor'
import FontFamily from '@tiptap/extension-font-family'
import TextStyle from '@tiptap/extension-text-style'
import CharacterCount from '@tiptap/extension-character-count'
import Underline from '@tiptap/extension-underline'
import Superscript from '@tiptap/extension-superscript'
import Subscript from '@tiptap/extension-subscript'
import Strike from '@tiptap/extension-strike'
import Link from '@tiptap/extension-link'
import Italic from '@tiptap/extension-italic'
import Bold from '@tiptap/extension-bold'
import Highlight from '@tiptap/extension-highlight'
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight'
import { all, createLowlight } from 'lowlight'
import HardBreak from '@tiptap/extension-hard-break'
import Heading from '@tiptap/extension-heading'
import OrderedList from '@tiptap/extension-ordered-list'
import HorizontalRule from '@tiptap/extension-horizontal-rule'
import Youtube from '@tiptap/extension-youtube'

const lowlight = createLowlight(all)

export default {
  components: {
    EditorContent
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    edit: {
      type: Boolean,
      default: false
    },
    limit: {
      type: Number,
      default: 5000
    },
    placeholder: {
      type: String,
      default: 'Write something ...'
    }
  },
  data () {
    return {
      editor: null,
      width: 640,
      height: 480,
      table_size_menu_visiable: false
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
    extractWords: function (text) {
      const cleanText = text.replace(/[.,!?;:]/g, '').toLowerCase()
      const words = cleanText.split(/\s+/)
      return words.filter(word => word.length > 0)
    },
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
    },
    addVideo: function () {
      const url = prompt('Enter YouTube URL')

      this.editor.commands.setYoutubeVideo({
        src: url,
        width: Math.max(320, parseInt(this.width, 10)) || 640,
        height: Math.max(180, parseInt(this.height, 10)) || 480
      })
    },
    setLink: function () {
      const previousUrl = this.editor.getAttributes('link').href
      const url = window.prompt('URL', previousUrl)

      // cancelled
      if (url === null) {
        return
      }

      // empty
      if (url === '') {
        this.editor
          .chain()
          .focus()
          .extendMarkRange('link')
          .unsetLink()
          .run()

        return
      }

      // update link
      this.editor
        .chain()
        .focus()
        .extendMarkRange('link')
        .setLink({ href: url })
        .run()
    }
  },
  mounted () {
    // Configure Table Dropdown Menu Events
    this.$root.$on('bv::dropdown::show', bvEvent => {
      if (bvEvent.componentId === 'tablesizemenu') {
        this.table_size_menu_visiable = true
      }
    })
    this.$root.$on('bv::dropdown::hide', bvEvent => {
      if (bvEvent.componentId === 'tablesizemenu') {
        this.table_size_menu_visiable = false
      }
      if (this.table_size_menu_visiable) {
        bvEvent.preventDefault()
      }
    })

    // Configure Editor
    this.editor = new Editor({
      content: this.value,
      editable: this.edit,
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

            return this.placeholder
          },
          showOnlyWhenEditable: true
        }),
        ListKeymap,
        Gapcursor,
        FontFamily,
        TextStyle,
        CharacterCount.configure({
          limit: this.limit
        }),
        Underline,
        Superscript,
        Subscript,
        Strike,
        Link,
        Italic,
        Bold,
        Highlight.configure({ multicolor: true }),
        CodeBlockLowlight.configure({
          lowlight
        }),
        HardBreak,
        Heading.configure({
          levels: [3, 4, 5]
        }),
        OrderedList,
        HorizontalRule,
        Youtube.configure({
          controls: false,
          nocookie: true
        })
      ],
      onUpdate: () => {
        // HTML
        this.$emit('input', this.editor.getHTML())

        // JSON
        // this.$emit('input', this.editor.getJSON())
      }
    })
  },
  computed: {
    percentage: function () {
      return Math.round((100 / this.limit) * this.editor.storage.characterCount.characters())
    }
  },
  beforeDestroy () {
    this.editor.destroy()
  }
}
</script>

<style lang="scss">

.stripped-dropdown {
  background-color: transparent;
  border: none;
  box-shadow: none;
  border-radius: 0;
}

.is-active {
  background-color:#457fa8 !important;
  color: white !important;
}

.text-editor-button {
  border-width: 1px;
  border-color:#999999;
}

.text-editor-button.disabled {
  border-width: 1px;
  border-color:#CCCCCC;
}

.character-count {
  align-items: center;
  color: var(--gray-5);
  display: flex;
  font-size: 0.75rem;
  gap: .5rem;
  margin: 1.5rem;

  svg {
    color: var(--purple);
  }

  &--warning,
  &--warning svg {
    color: var(--red);
  }
}

/* Basic editor styles */
.tiptap:focus {
  outline: none;
}

.tiptap {
  padding: 1rem;

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

  hr {
    border: none;
    border-top: 1px solid var(--gray-2);
    cursor: pointer;
    margin: 2rem 0;

    &.ProseMirror-selectednode {
      border-top: 1px solid var(--purple);
    }
  }

  blockquote {
    border-left: 3px solid var(--gray-3);
    margin: 1.5rem 0;
    padding-left: 1rem;
  }

  pre {
    background: black;
    border-radius: 0.5rem;
    color: white;
    font-family: 'JetBrainsMono', monospace;
    margin: 1.5rem 0;
    padding: 0.75rem 1rem;

    code {
      background: none;
      color: inherit;
      font-size: 0.8rem;
      padding: 0;
    }

    /* Code styling */
    .hljs-comment,
    .hljs-quote {
      color: #616161;
    }

    .hljs-variable,
    .hljs-template-variable,
    .hljs-attribute,
    .hljs-tag,
    .hljs-name,
    .hljs-regexp,
    .hljs-link,
    .hljs-name,
    .hljs-selector-id,
    .hljs-selector-class {
      color: #f98181;
    }

    .hljs-number,
    .hljs-meta,
    .hljs-built_in,
    .hljs-builtin-name,
    .hljs-literal,
    .hljs-type,
    .hljs-params {
      color: #fbbc88;
    }

    .hljs-string,
    .hljs-symbol,
    .hljs-bullet {
      color: #b9f18d;
    }

    .hljs-title,
    .hljs-section {
      color: #faf594;
    }

    .hljs-keyword,
    .hljs-selector-tag {
      color: #70cff8;
    }

    .hljs-emphasis {
      font-style: italic;
    }

    .hljs-strong {
      font-weight: 700;
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

  mark {
    background-color: #FAF594;
    border-radius: 0.4rem;
    box-decoration-break: clone;
    padding: 0.1rem 0.3rem;
  }

  /* List styles */
  ul,
  ol {
    padding: 0 1rem;
    margin: 1.25rem 1rem 1.25rem 0.4rem;

    li p {
      margin-top: 0.25em;
      margin-bottom: 0.25em;
    }
  }
}
</style>
