<template>
  <div class="my_component">
    <div
      v-b-visible="handleVisible"
      class="position-fixed d-block d-lg-none"
      style="z-index: 20000; height: 1px;"
    ></div>
    <div>
      <b-sidebar id="sidebar-right" :title="data.title" :right="true" shadow :lazy="true" backdrop-variant="dark" :no-close-on-route-change="true">
        <div class="mx-2">
          <div class="mx-2 mb-3 mt-0">
            <strong>Revision No.: {{ data.revision }}</strong><br>
            <strong>Issued Date: {{ new Date(data.timestamp_issued).toLocaleDateString('en-US') }}</strong><br>
            <strong>Review Date: {{ new Date(data.timestamp_modified).toLocaleDateString('en-US') }}</strong>
          </div>
          <b-form-textarea v-model="data.description" no-resize disabled></b-form-textarea>
          <div class="my-3" style="position:relative; height:300px; overflow-y:scroll;">
            <b-navbar v-b-scrollspy style="width: 100%;">
              <b-nav pills vertical class="accordion" style="width: 100%;">
                <div v-for="(chapter, chapter_loop_key) in data.chapters" :key="chapter_loop_key">
                  <b-nav-item @click="changeChapter(chapter_loop_key)" v-b-toggle="`accordion-${chapter_loop_key}`" v-b-tooltip.hover :title="chapter.description">
                    <div class="d-flex flex-row justify-content-between">
                      <div>{{ chapter.title }}</div>
                      <b-icon icon="chevron-compact-down"></b-icon>
                    </div>
                  </b-nav-item>
                  <b-nav pills>
                    <b-collapse :id="`accordion-${chapter_loop_key}`" accordion="my-accordion" role="tabpanel" style="width: 100%;">
                      <div v-for="(section, section_key) in data.chapters[chapter_loop_key].sections" :key="`SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`">
                        <b-nav-item class="ml-3 my-1" :href="`#SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`" @click="scrollIntoView($event, `SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`)">
                          <div class="d-flex flex-row justify-content-between">
                            <div>{{ section.title }}</div>
                          </div>
                        </b-nav-item>
                      </div>
                    </b-collapse>
                  </b-nav>
                </div>
              </b-nav>
            </b-navbar>
          </div>
        </div>
      </b-sidebar>
    </div>
    <b-container class="p-0 m-2" fluid style="max-width: 96%;">
      <b-row class="mx-2" cols="1" cols-lg="2">
        <b-col class="p-1 d-flex justify-content-end" lg="3" v-if="!isMd">
          <b-card class="position-fixed mr-2" style="width: 20%;">
            <b-card-title @click="chapter_key=''" style="cursor: pointer;"><h1>{{ data.title}}</h1></b-card-title>
            <b-card-sub-title v-show="data?.subtitle">{{ data.subtitle }}</b-card-sub-title>
            <b-card-body class="pl-0" style="width: 100%;">
              <div class="mx-2 mb-3 mt-0">
                <strong>Revision No.: {{ data.revision }}</strong><br>
                <strong>Issued Date: {{ new Date(data.timestamp_issued).toLocaleDateString('en-US') }}</strong><br>
                <strong>Review Date: {{ new Date(data.timestamp_modified).toLocaleDateString('en-US') }}</strong>
              </div>
              <b-form-textarea v-model="data.description" no-resize disabled></b-form-textarea>
              <div class="my-3" style="position:relative; height:300px; overflow-y:scroll;">
                <b-navbar v-b-scrollspy style="width: 100%;">
                  <b-nav pills vertical class="accordion" style="width: 100%;">
                    <div v-for="(chapter, chapter_loop_key) in data.chapters" :key="chapter_loop_key">
                      <b-nav-item @click="changeChapter(chapter_loop_key)" v-b-toggle="`accordion-${chapter_loop_key}`" v-b-tooltip.hover :title="chapter.description">
                        <div class="d-flex flex-row justify-content-between">
                          <div>{{ chapter.title }}</div>
                          <b-icon icon="chevron-compact-down"></b-icon>
                        </div>
                      </b-nav-item>
                      <b-nav pills>
                        <b-collapse :id="`accordion-${chapter_loop_key}`" accordion="my-accordion" role="tabpanel" style="width: 100%;">
                          <div v-for="(section, section_key) in data.chapters[chapter_loop_key].sections" :key="`SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`">
                            <b-nav-item class="ml-3 my-1" :href="`#SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`" @click="scrollIntoView($event, `SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`)">
                              <div class="d-flex flex-row justify-content-between">
                                <div>{{ section.title }}</div>
                              </div>
                            </b-nav-item>
                          </div>
                        </b-collapse>
                      </b-nav>
                    </div>
                  </b-nav>
                </b-navbar>
              </div>
            </b-card-body>
          </b-card>
        </b-col>
        <b-col class="p-1 d-flex justify-content-start" lg="9" style="width: 100%;">
          <b-card class="custom-content-card" v-if="chapter_key">
            <div v-if="!chapter_loaded" class="d-flex justify-content-center my-3">
              <b-spinner label="Loading..." variant="primary"></b-spinner>
            </div>
            <div v-show="chapter_loaded">
              <b-card-title class="input-group d-flex justify-content-between px-3 pt-3">
                <h2>{{ data.chapters[chapter_key].title }}</h2>
                <h3 v-if="!isMd">SOP {{ data.abv }} {{chapter_key}}</h3>
                <b-button v-if="isMd" v-b-tooltip.hover title="Table of Contents" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light ml-3" type="button" id="button-addon2">
                  <b-icon icon="list"></b-icon>
                </b-button>
              </b-card-title>
              <b-card-sub-title v-if="isMd" class="px-3"><strong>SOP {{ data.abv }} {{chapter_key}} | </strong><span v-show="data.chapters[chapter_key]?.subtitle">{{ data.chapters[chapter_key].subtitle }}</span></b-card-sub-title>
              <b-card-body class="px-0">
                <div class="d-flex flex-row justify-content-between mx-4" style="border-bottom: 1px solid #999999;">
                  <div>
                    <h4 style="font-family: Garamond, sans-serif; color:#7f8c3c;"><strong>Chapter Details</strong><b-button @click="setEditButton(`SOP-${data.abv}-${data.document_id}-${chapter_key}-00`)" v-show="!edit" v-b-tooltip.hover title="Edit Chapter Details" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h4>
                  </div>
                </div>
                <b-container class="my-2">
                  <b-row class="ml-2 mb-3">
                    <b-col md="4">
                      <strong>Revision No.: {{ data.chapters[chapter_key].revision }}</strong>
                    </b-col>
                    <b-col md="4">
                      <strong>Issued Date: {{ new Date(data.chapters[chapter_key].timestamp_issued).toLocaleDateString('en-US') }}</strong>
                    </b-col>
                    <b-col md="4">
                      <strong>Review Date: {{ new Date(data.chapters[chapter_key].timestamp_modified).toLocaleDateString('en-US') }}</strong>
                    </b-col>
                  </b-row>
                </b-container>
                <b-container class="mb-3 mx-2">
                  <h5 class="ml-1">Authors</h5>
                  <b-container class="d-flex">
                    <div v-for="(author, author_key) in data.chapters[chapter_key].authors" :key="author_key" class="mx-2">
                      <b-avatar :id="`popover-${author.user_id}`" :text="author.first_name[0] + author.last_name[0]" size="2.5rem" class="mr-1 mb-1"></b-avatar>
                      <b-popover :target="`popover-${author.user_id}`" triggers="hover" placement="top">
                        <template #title>{{ author.first_name }} {{ author.last_name}}</template>
                        Last Edit: {{ new Date(author.date_edited).toLocaleDateString('en-US') }}
                      </b-popover>
                    </div>
                    <div v-if="data.chapters[chapter_key].authors.length === 0" class="mr-1 mb-1">
                      <b-card-text>No Authors</b-card-text>
                    </div>
                  </b-container>
                </b-container>
                <b-container class="mb-3 mx-2">
                  <h5 class="ml-1">Tagged Regulations</h5>
                  <b-container class="d-flex flex-wrap">
                    <div v-for="(regulation, index) in data.chapters[chapter_key].regulations" :key="index" class="mr-1 mb-1">
                      <FedRegulation :regulation="regulation" />
                    </div>
                    <div v-if="data.chapters[chapter_key].regulations.length === 0 && edit !== `SOP-${data.abv}-${data.document_id}-${chapter_key}-00`" class="mr-1 mb-1">
                      <b-card-text>No Tagged Regulations</b-card-text>
                    </div>
                    <b-button @click="addRegulation()" v-show="edit === `SOP-${data.abv}-${data.document_id}-${chapter_key}-00`" pill variant="light" class="p-2 m-2" style="border: 1px solid black;">
                      <b-icon icon="plus"></b-icon>
                    </b-button>
                  </b-container>
                </b-container>
                <b-container class="mb-3 mx-2">
                  <h5 class="ml-1">Description</h5>
                  <b-form-textarea style="max-width: 80%;" v-model="data.chapters[chapter_key].description" no-resize disabled class="mx-4 my-2"></b-form-textarea>
                </b-container>
                <div class="d-flex my-3" v-if="edit === `SOP-${data.abv}-${data.document_id}-${chapter_key}-00`">
                  <b-button variant="outline-danger" class="m-2" @click="unsetEditButton()">Cancel</b-button>
                  <b-button variant="outline-success" class="m-2" @click="saveEdit()">Save</b-button>
                </div>
                <div v-for="(section, section_key) in data.chapters[chapter_key].sections" :key="`SOP-${data.abv}-${data.document_id}-${chapter_key}-${section_key}`">
                  <div class="d-flex flex-row justify-content-between mx-4" style="border-bottom: 1px solid #999999;">
                    <div>
                      <h4 style="font-family: Garamond, sans-serif; color:#7f8c3c;" :id="`SOP-${data.abv}-${data.document_id}-${chapter_key}-${section_key}`"><strong>{{ section.title.toUpperCase() }}</strong><b-button @click="setEditButton(`SOP-${data.abv}-${data.document_id}-${chapter_key}-${section_key}`)" v-show="!edit" v-b-tooltip.hover title="Edit Section" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h4>
                      <span v-show="section?.subtitle">{{ section?.subtitle }}</span>
                    </div>
                    <strong>{{ data.abv }} {{ chapter_key }}.{{ section_key }}</strong>
                  </div>
                  <TipTap v-model="section.content" :edit="edit === `SOP-${data.abv}-${data.document_id}-${chapter_key}-${section_key}`" class="my-2"/>
                  <!-- {{ section.content }} -->
                  <div class="d-flex my-3" v-if="edit === `SOP-${data.abv}-${data.document_id}-${chapter_key}-${section_key}`">
                    <b-button variant="outline-danger" class="m-2" @click="unsetEditButton()">Cancel</b-button>
                    <b-button variant="outline-success" class="m-2" @click="saveEdit()">Save</b-button>
                  </div>
                </div>
              </b-card-body>
            </div>
          </b-card>
          <b-card class="custom-content-card" v-else>
            <div v-if="!chapter_loaded" class="d-flex justify-content-center my-3">
              <b-spinner label="Loading..." variant="primary"></b-spinner>
            </div>
            <div v-show="chapter_loaded">
              <b-card-title class="input-group d-flex justify-content-between px-3 pt-3">
                <h2>{{ data.title }}<b-button @click="setEditButton(`SOP-${data.abv}-${data.document_id}-${chapter_key}-00`)" v-show="!edit" v-b-tooltip.hover title="Edit Chapter Header" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h2>
                <h3 v-if="!isMd">SOP {{ data.abv }}</h3>
                <b-button v-if="isMd" v-b-tooltip.hover title="Table of Contents" v-b-toggle.sidebar-right style="border-width: 2px; border-color:#999999" class="btn my-2 mx-1 btn-light ml-3" type="button" id="button-addon2">
                  <b-icon icon="list"></b-icon>
                </b-button>
              </b-card-title>
              <b-card-sub-title v-if="isMd" class="px-3"><strong>SOP {{ data.abv }} | </strong><span v-show="data?.subtitle">{{ data.subtitle }}</span></b-card-sub-title>
              <b-card-body class="px-0">
                <div class="d-flex flex-row justify-content-between mx-4" style="border-bottom: 1px solid #999999;">
                  <div>
                    <h4 style="font-family: Garamond, sans-serif; color:#7f8c3c;"><strong>Document Details</strong><b-button @click="setEditButton(`SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`)" v-show="!edit" v-b-tooltip.hover title="Edit Section" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h4>
                  </div>
                </div>
                <b-container class="my-2">
                  <b-row class="ml-2 mb-3">
                    <b-col md="4">
                      <strong>Revision No.: {{ data.revision }}</strong>
                    </b-col>
                    <b-col md="4">
                      <strong>Issued Date: {{ new Date(data.timestamp_issued).toLocaleDateString('en-US') }}</strong>
                    </b-col>
                    <b-col md="4">
                      <strong>Review Date: {{ new Date(data.timestamp_modified).toLocaleDateString('en-US') }}</strong>
                    </b-col>
                  </b-row>
                </b-container>
                <b-container class="mb-3 mx-2">
                  <h5 class="ml-1">Authors</h5>
                  <b-container class="d-flex">
                    <div v-for="(author, author_key) in data.authors" :key="author_key" class="mx-2">
                      <b-avatar :id="`popover-${author.user_id}`" :text="author.first_name[0] + author.last_name[0]" size="2.5rem" class="mr-1 mb-1"></b-avatar>
                      <b-popover :target="`popover-${author.user_id}`" triggers="hover" placement="top">
                        <template #title>{{ author.first_name }} {{ author.last_name}}</template>
                        Last Edit: {{ new Date(author.date_edited).toLocaleDateString('en-US') }}
                      </b-popover>
                    </div>
                    <div v-if="data.chapters[chapter_key].authors.length === 0" class="mr-1 mb-1">
                      <b-card-text>No Authors</b-card-text>
                    </div>
                  </b-container>
                </b-container>
                <b-container class="mb-3 mx-2">
                  <h5 class="ml-1">Description</h5>
                  <b-form-textarea v-model="data.description" no-resize disabled class="my-2 ml-1"></b-form-textarea>
                </b-container>
                <div class="d-flex flex-row justify-content-between mx-4" style="border-bottom: 1px solid #999999;">
                  <div>
                    <h4 style="font-family: Garamond, sans-serif; color:#7f8c3c;"><strong>Table of Contents</strong></h4>
                  </div>
                </div>
                <div class="my-3" style="width: 100%;">
                  <b-navbar>
                    <b-nav pills vertical class="accordion">
                      <div v-for="(chapter, chapter_loop_key) in data.chapters" :key="chapter_loop_key">
                        <b-nav-item v-b-toggle="`accordion-${chapter_loop_key}`" v-b-tooltip.hover :title="chapter.description">
                          <div class="d-flex flex-row justify-content-between">
                            <div>SOP {{ data.abv }} {{ chapter_loop_key }} - {{ chapter.title }}</div>
                            <b-icon icon="chevron-compact-down" class="ml-3"></b-icon>
                          </div>
                        </b-nav-item>
                        <b-nav pills>
                          <b-collapse :id="`accordion-${chapter_loop_key}`" accordion="my-accordion" role="tabpanel" style="width: 100%;">
                            <div v-for="(section, section_key) in data.chapters[chapter_loop_key].sections" :key="`SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`">
                              <b-nav-item class="ml-3 my-1" :href="`#SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`" @click="changeChapterAndSection(chapter_loop_key, $event, `SOP-${data.abv}-${data.document_id}-${chapter_loop_key}-${section_key}`)">
                                <div class="d-flex flex-row justify-content-between">
                                  <div>SOP {{ data.abv }} {{ chapter_loop_key }}.{{ section_key }} - {{ section.title }}</div>
                                </div>
                              </b-nav-item>
                            </div>
                          </b-collapse>
                        </b-nav>
                      </div>
                    </b-nav>
                  </b-navbar>
                </div>
              </b-card-body>
            </div>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import TipTap from '@/components/TipTap.vue'
import SOPTemplate from './SOPTemplate.js'
import FedRegulation from './FedRegulation.vue'

export default {
  name: 'PoliciesHome',
  components: {
    TipTap,
    FedRegulation
  },
  data: function () {
    return {
      loaded: true,
      chapter_loaded: true,
      isMd: false,
      edit: '',
      content_buffer: '',
      data: JSON.parse(SOPTemplate),
      chapter_key: ''
    }
  },
  computed: {
    filterActive: function () {
      if (this.search_query.length > 0) {
        return true
      }
      return false
    }
  },
  methods: {
    saveEdit: function () {
      if (this.edit.slice(-2) !== '00') {
        this.addAuthor()
        this.updateChapterHeader()
        this.updateDocumentHeader()
      }
      this.unsetEditButton()
    },
    unsetEditButton: function () {
      this.edit = ''
      this.content_buffer = ''
    },
    setEditButton: function (id) {
      this.edit = id
    },
    updateDocumentHeader: function () {
      this.data.revision = this.data.revision + 1
      this.data.timestamp_modified = new Date().toISOString()
    },
    updateChapterHeader: function () {
      this.data.chapters[this.chapter_key].revision = this.data.chapters[this.chapter_key].revision + 1
      this.data.chapters[this.chapter_key].timestamp_modified = new Date().toISOString()
    },
    addAuthor: function () {
      const userData = {
        department: this.$root.userData.department,
        first_name: this.$root.userData.first_name,
        last_name: this.$root.userData.last_name,
        organization_id: this.$root.userData.organization_id,
        person_id: this.$root.userData.person_id,
        user_id: this.$root.userData.user_id,
        user_name: this.$root.userData.user_name,
        profile_picture: this.$root.userData.profile_picture,
        date_edited: new Date().toISOString()
      }
      this.data.chapters[this.chapter_key].authors[this.$root.userData.user_id] = userData
    },
    addRegulation: function () {
      const url = new URL(prompt('Enter www.ecfr.gov URL'))

      // check that url is referencing ecfr.gov
      if (url.hostname !== 'www.ecfr.gov') {
        alert('URL must be from www.ecfr.gov')
        return
      }

      const urlParts = url.pathname.split('/')

      // Handle Date, default null
      let regulationDate = null
      if (urlParts.length >= 1 && urlParts[1] !== 'current') {
        regulationDate = urlParts[1]
      }

      // Handle Title, default null
      let title = null
      if (urlParts.length >= 2 && urlParts[2].includes('title-')) {
        title = urlParts[2].replace('title-', '')
      }

      // Handle section, default null
      let section = null
      if (urlParts.length >= 3 && urlParts[3].includes('section-')) {
        section = urlParts[3].replace('section-', '')
        this.data.chapters[this.chapter_key].regulations.push({
          title: title,
          chapter: null,
          subchapter: null,
          part: null,
          subpart: null,
          regulation_date: regulationDate,
          section: section
        })
        return
      }

      // Handle Chapter, default null
      let chapter = null
      if (urlParts.length >= 3 && urlParts[3].includes('chapter-')) {
        chapter = urlParts[3].replace('chapter-', '')
      }

      // Handle Subchapter, default null
      let subchapter = null
      if (urlParts.length >= 4 && urlParts[4].includes('subchapter-')) {
        subchapter = urlParts[4].replace('subchapter-', '')
      }

      // Handle Part, default null
      let part = null
      if (urlParts.length >= 5 && urlParts[5].includes('part-')) {
        part = urlParts[5].replace('part-', '')
      }

      // Handle Subpart inside hash, default null
      let subpart = null
      if (url.hash) {
        subpart = url.hash.replace('#', '').split('.')[1]
      }

      this.data.chapters[this.chapter_key].regulations.push({
        title: title,
        chapter: chapter,
        subchapter: subchapter,
        part: part,
        subpart: subpart,
        regulation_date: regulationDate,
        section: section
      })
    },
    info: function (item, index, button) {
      this.infoModal.title = `Row index: ${index}`
      this.infoModal.content = JSON.stringify(item, null, 2)
      this.$root.$emit('bv::show::modal', this.infoModal.id, button)
    },
    resetInfoModal: function () {
      this.infoModal.title = ''
      this.infoModal.content = ''
    },
    clearSearch: function () {
      this.search_query = ''
      this.search_query_buff = ''
    },
    search: function () {
      this.search_query = this.search_query_buff
    },
    handleVisible: function (isVisible) {
      this.isMd = isVisible
    },
    scrollIntoView: function (event, id) {
      event.preventDefault()
      const el = document.getElementById(id)
      if (el) {
        window.scrollTo({
          top: el.offsetTop - 40,
          behavior: 'smooth'
        })
      } else if (this.$route.hash) {
        this.$router.push({
          name: 'NotFound'
        })
      }
    },
    changeChapter: function (chapterKey) {
      if (this.chapter_key === chapterKey) {
        return true
      }
      this.chapter_loaded = false
      window.scrollTo({ top: 0 })
      this.chapter_key = chapterKey
      // wait for a second then display chapter
      const myPromise = new Promise((resolve, reject) => {
        setTimeout(() => {
          this.chapter_loaded = true
          resolve(true)
        }, 1000)
      })
      return myPromise
    },
    changeChapterAndSection: async function (chapterKey, event, id) {
      await this.changeChapter(chapterKey)
      this.scrollIntoView(event, id)
    }
  },
  created: function () {
    if (this.$route.hash) {
      const [abv, documentId, chapterKey, sectionKey] = this.$route.hash.replace('#', '').replace('SOP-', '').split('-')

      const chapterIds = Object.keys(this.data.chapters)

      if (!chapterIds.includes(chapterKey)) {
        this.$router.push({
          name: 'NotFound'
        })
        return
      }

      this.changeChapterAndSection(chapterKey, { preventDefault: () => {} }, `SOP-${abv}-${documentId}-${chapterKey}-${sectionKey}`)
    }
  }
}
</script>

<style scoped>
.my_component {
  width: 95%;
}

.custom-scrollspy {
  position: relative;
  overflow-y: auto;
  height: 38vw;
}

.custom-content-card {
  width: 100%;
}

@media (max-width: 1200px) {
  .my_component {
    width: 100%;
  }

  .custom-scrollspy {
    height: 100%;
  }

  .custom-content-card {
    width: 100%;
  }
}
</style>
