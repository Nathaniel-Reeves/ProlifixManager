<template>
  <div class="my_component d-flex flex-wrap justify-content-center" v-on:keydown.ctrl.80.exact="renderPrint($event)">
    <div class="card my-2" v-if="!loaded" style="box-shadow: 0 20px 40px rgba(0,0,0,.2);">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid class="p-0">
      <b-card class="my-2" v-if="loaded" style="box-shadow: 0 20px 40px rgba(0,0,0,.2);">
        <b-card-body>
          <div class="card-title d-flex align-items-center flex-wrap">
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2 m-3" src="../../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <div>
              <div class="card-title d-flex align-items-center">
                <h1>{{ product_data.product_name }}</h1>
                <CertBadge :data="product_data" :print-icon="true"></CertBadge>
              </div>
              <router-link :to="'/organizations/'+product_data.organization_id" target="_blank"><h4 class="card-subtitle text-muted mb-2">{{ product_data.organization_name }} {{ product_data.organizaiton_initial ? '(' + product_data.organizaiton_initial + ')' : '' }}</h4></router-link>
            </div>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#ProductVariants" @click="scrollIntoView" :disabled="!activeSection('variants')">Product Variants</b-nav-item>
            <b-nav-item href="#Labels" @click="scrollIntoView" :disabled="!activeSection('labels')">Labels</b-nav-item>
            <b-nav-item href="#Formulas" @click="scrollIntoView" :disabled="!activeSection('formulas')">Formulas</b-nav-item>
            <b-nav-item href="#FormulaDocuments" @click="scrollIntoView" :disabled="!activeSection('formula_docs')">Formula Documents</b-nav-item>
            <b-nav-item href="#Manufacturing" @click="scrollIntoView" :disabled="!activeSection('manufacturing')">Manufacturing</b-nav-item>
            <b-nav-item href="#ComponentsSummary" @click="scrollIntoView" :disabled="edit_manufacturing || edit_manufacturing_docs || edit_formulas || edit_formula_docs || edit_specs || edit_labels || edit_variants">Components Summary</b-nav-item>
            <b-nav-item href="#ManufacturingDocuments" @click="scrollIntoView" :disabled="!activeSection('manufacturing_docs')">Manufacturing Documents</b-nav-item>
            <b-nav-item href="#Specifications" @click="scrollIntoView" v-if="product_data.doc.specifications !== undefined" :disabled="!activeSection('specs')">Specifications</b-nav-item>
            <div v-for="(spec, spec_key) in product_data.doc.specifications.specs" :key="spec_key">
              <b-nav-item :href="'#'+spec_key" @click="scrollIntoView" :disabled="!activeSection('specs')">{{ spec.test_name }}</b-nav-item>
            </div>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class="my-2" v-if="loaded" style="box-shadow: 0 20px 40px rgba(0,0,0,.2);">
        <hr class="d-none d-print-block">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">
          <ProductVariant
            v-show="activeSection('variants')"
            :product-id="product_data.product_id"
            :timestamp-fetched="product_data.timestamp_fetched"
            :num-variants="product_data.num_product_variants"
            :product-variants="product_data.product_variants"
            v-on:edit-variants="(e) => {edit_variants = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></ProductVariant>
          <hr v-show="activeSection('variants')">
          <ProductLabel
            v-show="activeSection('labels')"
            :id="product_data.product_id"
            :doc="product_data.doc"
            :name="product_data.product_name"
            :timestamp-fetched="product_data.timestamp_fetched"
            :variant_options="product_data.product_variants"
            v-on:edit-labels="(e) => {edit_labels = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></ProductLabel>
          <hr v-show="activeSection('labels')">
          <ProductFormula
            v-show="activeSection('formulas')"
            :v-key="formula_key"
            :product-id="product_data.product_id"
            :organic="product_data.certified_usda_organic"
            :formulas="product_data.formulas"
            :timestamp-fetched="product_data.timestamp_fetched"
            :num-versions="product_data.num_formula_versions"
            :default-formula-id="product_data.default_formula_version"
            v-on:edit-formulas="(e) => {edit_formulas = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></ProductFormula>
          <hr v-show="activeSection('formulas')">
          <div v-show="activeSection('formula_docs')" class="d-print-none">
            <h3 id="FormulaDocuments">Formula Documents<b-button v-if="!edit_formula_docs" v-b-tooltip.hover title="Edit Formula Documents" @click="toggleEditFormulaDocs()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
            <b-card-group class="ml-3">
              <div v-for="(document, index) in product_data.doc.formula_files" :key="index">
                <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                  <b-card-body>
                    <b-card-title class="my-1" v-show="document.document_type">
                      {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                      {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                      {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                      {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                      {{ document.document_type === 'audit' ? 'Audit' : null }}
                      {{ document.document_type === 'letter' ? 'Letter' : null }}
                      {{ document.document_type === 'other' ? 'Other' : null }}
                    </b-card-title>
                    <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                      :options="[
                        // { value: 'questionnaire', text: 'Questionnaire' },
                        // { value: 'certificate', text: 'Certificate' },
                        { value: 'food_safety_plan', text: 'Food Safety Plan' },
                        { value: 'flow_chart', text: 'Flow Chart' },
                        { value: 'audit', text: 'Audit' },
                        { value: 'letter', text: 'Letter' },
                        { value: 'other', text: 'Other' }
                      ]">
                    </v-select>
                    <strong>Document Name: </strong><br><b-form-input :disabled="!edit_formula_docs" v-model="document.name" type="text" class="my-1"></b-form-input>
                    <strong>Description: </strong><br><b-form-textarea :disabled="!edit_formula_docs" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                    <b-form-file v-if="!document.file_hash && edit_formula_docs" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                    <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                  </b-card-body>
                  <b-card-footer>
                    <b-button block v-show="edit_formula_docs" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(product_data.doc.formula_files, document)">Delete Document</b-button>
                    <div v-show="!edit_formula_docs">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                  </b-card-footer>
                </b-card>
              </div>
              <b-card class="m-2" v-if="edit_formula_docs" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(product_data.doc.formula_files, 'formula_documents')">
                <b-card-title>Add Document</b-card-title>
              </b-card>
              <b-card v-if="!edit_formula_docs && !(product_data?.doc?.formula_files?.length !== 0)">
                <b-card-title>No Formula Documents Yet</b-card-title>
              </b-card>
            </b-card-group>
            <div class="d-flex my-3">
              <div v-show="edit_formula_docs">
                <b-button type="submit" variant="outline-success" class="m-2" v-on:click="saveFormulaDocs()">Save</b-button>
                <b-button variant="outline-danger" class="m-2" v-on:click="toggleEditFormulaDocs()">Cancel</b-button>
              </div>
            </div>
          </div>
          <hr v-show="activeSection('formula_docs')" class="d-print-none">
          <ProductManufacturing
            class="d-print-none"
            v-show="activeSection('manufacturing')"
            :product-id="product_data.product_id"
            :manufacturing="product_data.manufacturing"
            :edit="edit_manufacturing"
            :variant_options="product_data.product_variants"
            :timestamp-fetched="product_data.timestamp_fetched"
            v-on:edit-manufacturing="(e) => {edit_manufacturing = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></ProductManufacturing>
          <hr v-show="activeSection('manufacturing')" class="d-print-none">
          <ProductManufacturing
            v-if="print"
            :product-id="product_data.product_id"
            :manufacturing="product_data.manufacturing"
            :edit="edit_manufacturing"
            :variant_options="product_data.product_variants"
            :timestamp-fetched="product_data.timestamp_fetched"
            v-on:edit-manufacturing="(e) => {edit_manufacturing = e}"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
            :print="true"
          ></ProductManufacturing>
          <hr v-show="activeSection('manufacturing')" class="d-none d-print-block">
          <div v-show="!edit_manufacturing & !edit_manufacturing_docs & !edit_formulas & !edit_formula_docs & !edit_specs & !edit_labels & !edit_variants">
            <h3 id="ComponentsSummary">Components Summary</h3>
            <b-table :items="components" :fields="component_fields" striped bordered sticky-header head-variant="light" style="max-height: 600px; min-width: 1100px;" show-empty :empty-text="'No Components Selected for this Process'">
              <template #cell(components)="components">
                <div v-for="(comp, index) in components.value" :key="comp.component_id+'-components'">
                  <b-row align-v="baseline" class="flex-nowrap">
                    <b-col cols="1">
                      <b-badge :id="comp.component_id+'-components-priority'" v-bind:variant="(comp.priority === 1 ? 'primary' : 'light')" pill class="ml-2 mt-3">{{ comp.priority }}</b-badge>
                      <b-tooltip :target="comp.component_id+'-components-priority'" triggers="hover">Priority Level: {{ comp.priority }}</b-tooltip>
                    </b-col>
                    <b-col cols="6"><b-link :to="'/catalogue/components/'+comp.component_id" target="_blank"><p class="py-3">{{ comp.component_primary_name ? comp.component_primary_name : comp.component_name }}</p></b-link></b-col>
                    <b-col><CertBadge :data="comp"></CertBadge></b-col>
                  </b-row>
                  <hr v-show="index < components.value.length-1">
                </div>
              </template>
              <template #cell(brands)="brands">
                <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                  <p class="py-3">
                    <b-badge :id="brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill class="mr-2">{{ brand.priority }}</b-badge>
                    <b-tooltip :target="brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                    <span :id="brand.organization_id+'-org-name'">{{ brand.organization_initial }}</span>
                    <b-tooltip :target="brand.organization_id+'-org-name'" triggers="hover">{{ brand.organization_name }}</b-tooltip>
                  </p>
                  <hr v-show="index < brands.value.length-1">
                </div>
              </template>
              <template #cell(qty_per_unit)="qty_per_unit">
                <strong style="font-size: 1.5em;">{{ qty_per_unit.value }}</strong>
              </template>
              <template #cell(specific_brand_required)="specific_brand_required">
                <span v-if="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
              </template>
              <template #cell(specific_component_required)="specific_component_required">
                <span v-if="specific_component_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
              </template>
            </b-table>
          </div>
          <hr v-show="!edit_manufacturing & !edit_manufacturing_docs & !edit_formulas & !edit_formula_docs & !edit_specs & !edit_labels & !edit_variants">
          <div v-show="activeSection('manufacturing_docs')" class="d-print-none">
            <h3 id="ManufacturingDocuments">Manufacturing Documents<b-button v-if="!edit_manufacturing_docs" v-b-tooltip.hover title="Edit Manufacturing Documents" @click="toggleEditManufacturingDocs()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
            <b-card-group class="ml-3">
              <div v-for="(document, index) in product_data.doc.manufacturing_files" :key="index">
                <b-card class="m-2" style="min-width: 22rem; max-width: 22rem;" no-body>
                  <b-card-body>
                    <b-card-title class="my-1" v-show="document.document_type">
                      {{ document.document_type === 'questionnaire' ? 'Questionnaire' : null }}
                      {{ document.document_type === 'certificate' ? 'Certificate' : null }}
                      {{ document.document_type === 'food_safety_plan' ? 'Food Safety Plan' : null }}
                      {{ document.document_type === 'flow_chart' ? 'Flow Chart' : null }}
                      {{ document.document_type === 'audit' ? 'Audit' : null }}
                      {{ document.document_type === 'letter' ? 'Letter' : null }}
                      {{ document.document_type === 'other' ? 'Other' : null }}
                    </b-card-title>
                    <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                      :options="[
                        // { value: 'questionnaire', text: 'Questionnaire' },
                        // { value: 'certificate', text: 'Certificate' },
                        { value: 'food_safety_plan', text: 'Food Safety Plan' },
                        { value: 'flow_chart', text: 'Flow Chart' },
                        { value: 'audit', text: 'Audit' },
                        { value: 'letter', text: 'Letter' },
                        { value: 'other', text: 'Other' }
                      ]">
                    </v-select>
                    <strong>Document Name: </strong><br><b-form-input :disabled="!edit_manufacturing_docs" v-model="document.name" type="text" class="my-1"></b-form-input>
                    <strong>Description: </strong><br><b-form-textarea :disabled="!edit_manufacturing_docs" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                    <b-form-file v-if="!document.file_hash && edit_manufacturing_docs" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                    <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                  </b-card-body>
                  <b-card-footer>
                    <b-button block v-show="edit_manufacturing_docs" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(product_data.doc.manufacturing_files, document)">Delete Document</b-button>
                    <div v-show="!edit_manufacturing_docs">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                  </b-card-footer>
                </b-card>
              </div>
              <b-card class="m-2" v-if="edit_manufacturing_docs" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(product_data.doc.manufacturing_files, 'manufacturing_documents')">
                <b-card-title>Add Document</b-card-title>
              </b-card>
              <b-card v-if="!edit_manufacturing_docs && (product_data?.doc?.manufacturing_files?.length !== 0)">
                <b-card-title>No Manufacturing Documents Yet</b-card-title>
              </b-card>
            </b-card-group>
            <div class="d-flex my-3">
              <div v-show="edit_manufacturing_docs">
                <b-button type="submit" variant="outline-success" class="m-2" v-on:click="saveManufacturingDocs()">Save</b-button>
                <b-button variant="outline-danger" class="m-2" v-on:click="toggleEditManufacturingDocs()">Cancel</b-button>
              </div>
            </div>
          </div>
          <hr v-show="activeSection('manufacturing_docs')" class="d-print-none">
          <SpecificationsComponent
            v-show="activeSection('specs')"
            :doc="product_data.doc"
            :spectype="'product'"
            :timestamp-fetched="product_data.timestamp_fetched"
            :name="product_data.product_name"
            :id="product_data.product_id"
            v-on:edit-specs="(e) => edit_specs = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="(v) => refreshParent(v)"
          ></SpecificationsComponent>
        </b-card-body>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import CertBadge from '../../../components/CertBadge.vue'
import ProductFormula from './ProductFormula.vue'
import ProductLabel from './ProductLabel.vue'
import ProductManufacturing from './ProductManufacturing.vue'
import SpecificationsComponent from '../SpecificationsComponent.vue'
import ProductVariant from './ProductVariant.vue'
import { CustomRequest, genTempKey } from '../../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import vSelect from 'vue-select'

export default {
  name: 'ProductsDetail',
  components: {
    CertBadge,
    ProductFormula,
    ProductManufacturing,
    SpecificationsComponent,
    ProductLabel,
    ProductVariant,
    vSelect
  },
  data: function () {
    return {
      loaded: false,
      id: this.$route.params.id,
      product_data: {},
      edit_manufacturing: false,
      edit_manufacturing_docs: false,
      edit_formulas: false,
      edit_formula_docs: false,
      edit_specs: false,
      edit_labels: false,
      edit_variants: false,
      doc_buffer: {},
      del_url_previews: [],
      formula_key: 0,
      original_doc: {},
      req: new CustomRequest(this.$cookies.get('session')),
      component_fields: [
        { label: 'Component', key: 'components', tdClass: 'custom-row' },
        { label: 'Brands', key: 'brands', tdClass: 'custom-row' },
        { label: 'Qty', key: 'qty_per_unit', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Brand Specific', key: 'specific_brand_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Component Specific', key: 'specific_component_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Product Variant', key: 'variant_title', tdClass: ['align-middle', 'custom-row'], class: 'text-center' }
      ],
      print: false
    }
  },
  computed: {
    components: function () {
      const components = []
      for (let i = 0; i < this.product_data.manufacturing.nodes.length; i++) {
        let variant = { variant_title: 'N/A' }
        if (this.product_data.manufacturing.nodes[i].variant_id) {
          variant = this.product_data.product_variants.find(v => v.variant_id === this.product_data.manufacturing.nodes[i].variant_id)
        }
        for (let j = 0; j < this.product_data.manufacturing.nodes[i].process_components.length; j++) {
          const row = {
            ...this.product_data.manufacturing.nodes[i].process_components[j],
            variant_title: variant.variant_title
          }
          components.push(row)
        }
      }
      return components
    }
  },
  methods: {
    renderPrint: function (e) {
      e.preventDefault()
      this.print = true
      if (!this.loaded) {
        return false
      }
      // wait for the page to render before printing
      this.$nextTick(() => {
        setTimeout(() => {
          window.print()
          // wait before setting print to false
          setTimeout(() => {
            this.print = false
          }, 300)
        }, 1000)
      })
    },
    activeSection: function (section) {
      if (
        this.edit_manufacturing ||
        this.edit_manufacturing_docs ||
        this.edit_formulas ||
        this.edit_formula_docs ||
        this.edit_specs ||
        this.edit_labels ||
        this.edit_variants
      ) {
        if (section === 'manufacturing') {
          return this.edit_manufacturing
        }
        if (section === 'manufacturing_docs') {
          return this.edit_manufacturing_docs
        }
        if (section === 'formulas') {
          return this.edit_formulas
        }
        if (section === 'formula_docs') {
          return this.edit_formula_docs
        }
        if (section === 'specs') {
          return this.edit_specs
        }
        if (section === 'labels') {
          return this.edit_labels
        }
        if (section === 'variants') {
          return this.edit_variants
        }
        return !(
          this.edit_manufacturing ||
          this.edit_manufacturing_docs ||
          this.edit_formulas ||
          this.edit_formula_docs ||
          this.edit_specs ||
          this.edit_labels ||
          this.edit_variants
        )
      }
      return true
    },
    saveFormulaDocs: async function () {
      const createToast = this.$root.createToast
      this.loaded = false

      const updateProduct = {
        product_id: Number(this.id),
        timestamp_fetched: this.product_data.timestamp_fetched,
        doc: this.product_data.doc
      }

      this.req.upsertRecord('Product_Master', updateProduct)

      const resp = await this.req.sendRequest(window.origin)

      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status === 201) {
        this.req = new CustomRequest(this.$cookies.get('session'))
        this.edit_formula_docs = false
        this.getProductData()
        this.del_url_previews.forEach(url => URL.revokeObjectURL(url))
        return true
      }
      this.$root.handleStaleRequest(this.req.isStale(), window.location)
      this.loaded = true
      return false
    },
    saveManufacturingDocs: async function () {
      const createToast = this.$root.createToast
      this.loaded = false

      const updateProduct = {
        product_id: Number(this.id),
        doc: this.product_data.doc,
        timestamp_fetched: this.product_data.timestamp_fetched
      }

      this.req.upsertRecord('Product_Master', updateProduct)

      const resp = await this.req.sendRequest(window.origin)

      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status === 201) {
        this.req = new CustomRequest(this.$cookies.get('session'))
        this.edit_manufacturing_docs = false
        this.getProductData()
        this.del_url_previews.forEach(url => URL.revokeObjectURL(url))
        return true
      }
      this.$root.handleStaleRequest(this.req.isStale(), window.location)
      this.loaded = true
      return false
    },
    toggleEditFormulaDocs: function () {
      if (!this.edit_formula_docs) {
        this.original_doc = cloneDeep(this.product_data.doc)
      } else {
        this.product_data.doc = cloneDeep(this.original_doc)
      }
      this.edit_formula_docs = !this.edit_formula_docs
    },
    toggleEditManufacturingDocs: function () {
      if (!this.edit_formula_docs) {
        this.original_doc = cloneDeep(this.product_data.doc)
      } else {
        this.product_data.doc = cloneDeep(this.original_doc)
      }
      this.edit_manufacturing_docs = !this.edit_manufacturing_docs
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
        type: `products/${docType}`,
        id_code: `${this.product_data.product_name}_${this.id}_`,
        file_pointer: null,
        file_preview_pointer: null,
        file_type: null,
        url_preview: null,
        file_hash: null,
        date_uploaded: null
      }
      documents.push(document)
    },
    toggleLoaded: function (val) {
      this.loaded = val
    },
    refreshParent: function (val) {
      this.getProductData()
    },
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    getProductData: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/products?product-id=' + this.id + '&doc=true&populate=formulas&populate=product_variants&populate=manufacturing'
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
            this.product_data = data.data[0]
            // eslint-disable-next-line
            console.log(data)
            this.loaded = true
            this.edit_specs = false
            this.edit_manufacturing = false
            this.edit_formulas = false
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else if (response.status === 404) {
          this.$router.push({
            name: 'NotFound'
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
  watch: {
    product_data: function () {
      // refresh product formula if the formula data has changed in the parent.
      this.formula_key += 1
      this.edit_formulas = false
    }
  },
  created: function () {
    this.getProductData()
  }
}
</script>

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
