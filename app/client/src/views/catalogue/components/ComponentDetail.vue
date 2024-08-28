<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-if="!loaded" style="box-shadow: 0 20px 40px rgba(0,0,0,.2);">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid class="p-0">
      <b-card class=" my-2" v-if="loaded" style="box-shadow: 0 20px 40px rgba(0,0,0,.2);">
        <b-card-body>
          <div class="card-title d-flex align-items-center flex-wrap">
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2 m-3" src="../../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <h2 class="card-title">{{ get_component_primary_name(component_data) }} {{ format_string(component_data.component_type) }}</h2>
            <CertBadge :data="component_data" :print-icon="true"></CertBadge>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#Aliases" @click="scrollIntoView">Aliases</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView"
              v-if="component_data.doc.specifications !== undefined">Specifications</b-nav-item>
            <div v-if="component_data.doc.specifications !== undefined" class="d-flex">
              <div v-for="(spec, spec_key) in component_data.doc.specifications.specs" :key="spec_key">
                <b-nav-item :href="'#'+spec_key" @click="scrollIntoView">{{ spec.test_name }}</b-nav-item>
              </div>
            </div>
            <b-nav-item href="#MiscDocuments" @click="scrollIntoView">Miscellaneous Documents</b-nav-item>
            <b-nav-item href="#Label" v-show="component_data.is_label" @click="scrollIntoView">Label</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">

          <!-- Alias Names -->
          <NamesComponent
            :p-names="component_data.component_names"
            :id="component_data.component_id"
            :timestamp-fetched="component_data.timestamp_fetched"
            naming-type="component"
            :allow-edit="true"
            v-on:edit-names="(e) => edit_names = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="refreshParent"
          ></NamesComponent>
          <hr>

          <!-- Specifications -->
          <SpecificationsComponent
            v-if="component_data.doc.specifications !== undefined"
            :doc="component_data.doc"
            :spectype="'component'"
            :name="get_component_primary_name(component_data)"
            :id="component_data.component_id"
            :timestamp-fetched="component_data.timestamp_fetched"
            v-on:edit-specs="(e) => edit_specs = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></SpecificationsComponent>

          <!-- Documents -->
          <div v-show="!edit_specs && !edit_names" class="d-print-none">
            <h3 id="MiscDocuments">Miscellaneous Documents<b-button v-if="!edit_misc_doc" v-b-tooltip.hover title="Edit Miscellaneous Documents" @click="toggleEditMiscDocs()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
            <b-card-group class="ml-3">
              <div v-for="(document, index) in component_data.doc.documents" :key="index">
                <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                  <b-card-body>
                    <b-card-title class="my-1" v-show="document.document_type">
                      {{ document.document_type === 'spec_sheet' ? 'Spec Sheet' : null }}
                      {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                      {{ document.document_type === 'email' ? 'Email' : null }}
                      {{ document.document_type === 'letter' ? 'Letter' : null }}
                      {{ document.document_type === 'drawing' ? 'Drawing' : null }}
                      {{ document.document_type === 'bid' ? 'Bid' : null }}
                      {{ document.document_type === 'invoice' ? 'Invoice' : null }}
                      {{ document.document_type === 'other' ? 'Other' : null }}
                    </b-card-title>
                    <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                      :options="[
                        { value: 'spec_sheet', text: 'Spec Sheet' },
                        { value: 'certificate', text: 'Certificate' },
                        { value: 'email', text: 'Email' },
                        { value: 'letter', text: 'Letter' },
                        { value: 'drawing', text: 'Drawing' },
                        { value: 'bid', text: 'Bid' },
                        { value: 'invoice', text: 'Invoice' },
                        { value: 'other', text: 'Other' }
                      ]">
                    </v-select>
                    <strong>Document Name: </strong><br><b-form-input :disabled="!edit_misc_doc" v-model="document.name" type="text" class="my-1"></b-form-input>
                    <strong>Description: </strong><br><b-form-textarea :disabled="!edit_misc_doc" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                    <b-form-file v-if="!document.file_hash && edit_misc_doc" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                    <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                  </b-card-body>
                  <b-card-footer>
                    <b-button block v-show="edit_misc_doc" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(component_data.doc.documents, document)">Delete Document</b-button>
                    <div v-show="!edit_misc_doc">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                  </b-card-footer>
                </b-card>
              </div>
              <b-card class="m-2" v-if="edit_misc_doc" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(component_data.doc.documents, 'formula_documents')">
                <b-card-title>Add Document</b-card-title>
              </b-card>
              <b-card v-if="!edit_misc_doc && component_data.doc.documents.length === 0">
                <b-card-title>No Documents Yet</b-card-title>
              </b-card>
            </b-card-group>
            <div class="d-flex my-3">
              <div v-show="edit_misc_doc">
                <b-button type="submit" variant="outline-success" class="m-2" v-on:click="saveMiscDocs()">Save</b-button>
                <b-button variant="outline-danger" class="m-2" v-on:click="toggleEditMiscDocs()">Cancel</b-button>
              </div>
            </div>
          </div>
          <hr class="d-print-none">

          <!-- Label -->
          <div v-show="component_data.is_label">
            <h3 id="Label">Label</h3>
            <div class="d-flex justify-content-center">
              <b-overlay :show="component_data.doc.label.discontinued" :opacity="0.80" rounded="sm" @click="focus_label = !focus_label">
                <b-card no-body @click="focus_label = !focus_label" style="cursor: pointer;">
                  <b-card-img :src="label_image" style="min-height: 15rem; min-width: 20rem; max-height: 70rem; max-width: 90rem;"></b-card-img>
                  <b-card-body :overlay="true">
                    <div class="d-flex justify-content-between align-items-start flex-column" style="min-height: 100%;">
                      <div class="d-flex justify-content-between" style="min-width: 100%;">
                        <div>
                          <b-card v-show="focus_label">
                            <b-card-title>V{{ component_data.doc.label.label_version }}</b-card-title>
                            <b-card-sub-title>{{ component_data.doc.label.date_uploaded }} - Current</b-card-sub-title>
                            <div>
                              {{ getProductType(component_data.doc.label) }} ({{component_data.doc.label.qty}}
                                <span v-show="component_data.doc.label.product_type === 'capsule'">ct</span>
                                <span v-show="component_data.doc.label.product_type === 'powder'">g</span>
                                <span v-show="component_data.doc.label.product_type === 'liquid'">ml</span>)<br>
                              {{ getLabelType(component_data.doc.label) }}
                            </div>
                          </b-card>
                        </div>
                      </div>
                      <div>
                        <b-card no-body class="p-1" v-show="(component_data.doc.label.url_preview || component_data.doc.label.file_pointer) && focus_label && !isTempKey(component_data.doc.label.component_id)">
                          <b-button v-on:click.stop variant="light" :to="'/catalogue/products/'+component_data.doc.label.product_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
                        </b-card>
                      </div>
                    </div>
                  </b-card-body>
                </b-card>
                <template #overlay>
                  <div class="text-center">
                    <h3><b-badge v-show="component_data.doc.label.discontinued" variant="danger">Label Discontinued</b-badge></h3>
                    <b-form-textarea
                      v-show="component_data.doc.label.discontinued"
                      v-model="component_data.doc.label.discontinued_reason"
                      :disabled="true"
                      class="form-control my-2"
                      placeholder="Reason for Discontinuation"
                    ></b-form-textarea>
                  </div>
                </template>
              </b-overlay>
            </div>
          </div>

        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<style scoped>
.card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}
.scrollbox {
  position:relative;
  height:85vh;
  overflow-y:scroll;
}
.customize-table {
  --easy-table-body-item-padding:10px 10px 10px 10px;
}
.bold {
    font-weight: bold;
}
.my_component {
    width: 95%;
}
@media (max-width: 1024px) {
  .my_component {
      width: 98%;
  }
}
@media (max-width: 400px) {
  .my_component {
      width: 100%;
  }
}
@media print {
  .scrollbox {
    height: 100%;
    overflow-y:auto;
  }
  .my_component {
    width: 100%;
  }
}
</style>

<script>
import NamesComponent from './NamesComponent.vue'
import CertBadge from '../../../components/CertBadge.vue'
import SpecificationsComponent from '../SpecificationsComponent.vue'
import { cloneDeep } from 'lodash'
import compDoc from './compDocTemp.js'
import { CustomRequest, genTempKey, isTempKey } from '../../../common/CustomRequest.js'
import vSelect from 'vue-select'

export default {
  name: 'ComponentDetail',
  components: {
    NamesComponent,
    CertBadge,
    SpecificationsComponent,
    vSelect
  },
  data: function () {
    return {
      id: this.$route.params.id,
      component_data: {},
      loaded: false,
      edit_names: false,
      edit_specs: false,
      edit_misc_doc: false,
      original_doc: {},
      del_url_previews: [],
      focus_label: false,
      req: new CustomRequest(this.$cookies.get('session')),
      product_type_options: [
        {
          label: 'Capsule Fill',
          value: 'capsule'
        }, {
          label: 'Powder Fill',
          value: 'powder'
        }, {
          label: 'Liquid Fill',
          value: 'liquid'
        }
      ],
      label_type_options: [
        {
          label: 'Jar Label',
          value: 'label'
        }, {
          label: 'Pouch',
          value: 'pouch'
        }, {
          label: 'Carton',
          value: 'carton'
        }, {
          label: 'Promo Item',
          value: 'packaging_material'
        }
      ]
    }
  },
  methods: {
    isTempKey: function (key) {
      return isTempKey(key)
    },
    getLabelType: function (l) {
      return this.product_type_options.find((e) => e.value === l.product_type)?.label
    },
    getProductType: function (l) {
      return this.label_type_options.find((e) => e.value === l.label_type)?.label
    },
    toggleEditMiscDocs: function () {
      if (!this.edit_misc_doc) {
        this.original_doc = cloneDeep(this.component_data.doc)
      } else {
        this.component_data.doc = cloneDeep(this.original_doc)
      }
      this.edit_misc_doc = !this.edit_misc_doc
    },
    saveMiscDocs: async function () {
      const createToast = this.$root.createToast
      this.loaded = false

      const updateComponent = {
        component_id: Number(this.id),
        timestamp_fetched: this.component_data.timestamp_fetched,
        doc: this.component_data.doc
      }

      this.req.upsertRecord('Components', updateComponent)

      const resp = await this.req.sendRequest(window.origin)

      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status === 201) {
        this.req = new CustomRequest(this.$cookies.get('session'))
        this.edit_misc_doc = false
        this.getComponentData()
        this.del_url_previews.forEach(url => URL.revokeObjectURL(url))
        return true
      }
      this.$root.handleStaleRequest(this.req.isStale(), window.location)
      this.loaded = true
      return false
    },
    deleteDocument: function (documents, document) {
      this.$bvModal.msgBoxConfirm(`Are you sure you want to perminently delete '${document.name}' document?`).then(value => {
        if (value) {
          documents.splice(documents.findIndex((d) => d.id === document.id), 1)
          this.req.deleteFile(document.file_hash)
        }
      })
    },
    addDocument: function (documents, docType) {
      const document = {
        id: genTempKey(),
        description: null,
        name: null,
        type: `components/${docType}`,
        id_code: `${this.component_data.component_primary_name}_${this.id}_`,
        file_pointer: null,
        file_preview_pointer: null,
        file_type: null,
        url_preview: null,
        file_hash: null,
        date_uploaded: null
      }
      documents.push(document)
    },
    getFile: function (document) {
      if (document.file_hash) {
        const url = window.origin + '/api/v1/uploads/' + document.file_pointer
        return url
      } else {
        return document.url_preview
      }
    },
    onFileChange: async function (e, document) {
      if (e.target.files.length === 0) {
        return
      }

      // Preview File
      const file = e.target.files[0]
      document.date_uploaded = new Date().toISOString()
      document.id_code += document.document_type
      document.url_preview = URL.createObjectURL(file)
      this.del_url_previews.push(file)

      const customKey = await this.req.addFile(file, 1, document.id_code, document.type)
      document.file_pointer = customKey
    },
    toggleLoaded: function (val) {
      this.loaded = val
    },
    refreshParent: function (val) {
      this.getComponentData()
    },
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    format_string: function (type) {
      if (type === undefined) {
        return ''
      }
      return type.toLowerCase().split('_').map((s) => s.charAt(0).toUpperCase() + s.substring(1)).join(' ')
    },
    get_component_primary_name: function (component) {
      if (component.component_names !== undefined && component.component_names.length > 0) {
        for (let i = 0; i < component.component_names.length; i++) {
          if (component.component_names[i].primary_name) {
            return component.component_names[i].component_name
          }
        }
      }
      return 'No Name'
    },
    getComponentData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?component-id=' + this.id + '&populate=component_names&doc=true'
      // eslint-disable-next-line
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            this.component_data = data.data[0]
            if (!this.component_data?.doc) {
              this.component_data.doc = {}
            }
            if (!this.component_data.doc?.documents) {
              this.component_data.doc.documents = []
            }
            if (!this.component_data.doc?.label) {
              this.component_data.doc.label = compDoc.label
            }
            // eslint-disable-next-line
            console.log(this.component_data)
            this.loaded = true
          })
        } else if (response.status === 404) {
          this.$router.push({ path: '/404' })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
          console.log(response)
        }
      })
    }
  },
  computed: {
    label_image: function () {
      if (this.component_data.doc.label.file_pointer) {
        return window.origin + '/api/v1/uploads/' + this.component_data.doc.label.file_pointer
      } else {
        return ''
      }
    }
  },
  created: function () {
    this.getComponentData()
  }
}
</script>
