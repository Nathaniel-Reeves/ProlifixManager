<template>
  <div>
    <h3 id="Labels">Labels<b-button v-if="!edit_labels" v-b-tooltip.hover title="Edit Product Labels" @click="setLabelBuffer()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>

    <b-card-group deck style="width: 100%;">
      <div v-for="label, index in primaryLabels" :key="index" style="max-height: 30rem;" class="m-5">
        <b-card no-body @click="label.primary_focus = !label.primary_focus" style="cursor: pointer;">
          <b-card-img :src="label.url_preview ? label.url_preview : getFile(label.file_pointer)" style="max-height: 30rem;"></b-card-img>
          <b-card-body :overlay="true">
            <div class="d-flex justify-content-between align-items-start flex-column" style="min-height: 100%;">
              <div class="d-flex justify-content-between" style="min-width: 100%;">
                <div>
                  <b-card v-show="label.primary_focus">
                    <b-card-title>V{{ label.label_version }}<b-badge class="ml-3" variant="primary">Primary</b-badge></b-card-title>
                    <b-card-sub-title>{{ label.date_uploaded }} - Current</b-card-sub-title>
                    <div>
                      {{ getProductType(label) }} ({{label.qty}}
                        <span v-show="label.product_type === 'capsule'">ct</span>
                        <span v-show="label.product_type === 'powder'">g</span>
                        <span v-show="label.product_type === 'liquid'">ml</span>)<br>
                      {{ getLabelType(label) }}
                    </div>
                  </b-card>
                </div>
                <div v-show="label.primary_focus && edit_labels">
                  <b-button class="mr-2" @click="label.primary = false" variant="danger">Remove Primary</b-button>
                </div>
              </div>
              <div>
                <b-card no-body class="p-1" v-show="(label.url_preview || label.file_pointer) && label.primary_focus && !isTempKey(label.component_id)">
                  <b-button v-on:click.stop variant="light" :to="'/catalogue/components/'+label.component_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
                </b-card>
              </div>
            </div>
          </b-card-body>
        </b-card>
      </div>
      <div v-if="primaryLabels.length === 0">
        <b-card no-body>
          <b-card-img src="../../../assets/no_image_placeholder.png" style="max-height: 30rem;"></b-card-img>
          <b-card-body :overlay="true">
            <div class="d-flex justify-content-start">
              <div>
                <b-card>
                  <b-card-title>Primary Label <br> Not Set</b-card-title>
                </b-card>
              </div>
            </div>
          </b-card-body>
        </b-card>
      </div>
    </b-card-group>

    <div v-show="edit_labels" class="mt-3">
      <b-button class="mr-2" variant="outline-success" @click="submit()">Save</b-button>
      <b-button variant="outline-danger" @click="cancel()">Cancel</b-button>
    </div>

    <div class="d-flex justify-content-center d-print-none">
      <b-button v-show="!show_files" @click="show_files = true" class="m-1" variant="light">View All Labels</b-button>
      <b-button v-show="show_files" @click="show_files = false" class="m-1" variant="light">Hide Labels</b-button>
    </div>
    <b-collapse id="show_files d-print-none" v-model="show_files">
      <hr>
      <b-card-group deck style="width: 100%;">
        <div v-for="(label, index) in edit_labels_buffer.all_labels" v-show="!label.primary" :key="index" style="max-height: 30rem;" class="m-5">
          <b-overlay :show="label.discontinued" :opacity="0.80" rounded="sm" @click="label.focus = !label.focus">
            <b-card no-body @click="label.focus = !label.focus && label.buffered" style="cursor: pointer;">
              <b-card-img :src="label.url_preview || label.url_preview === null ? label.url_preview : getFile(label.file_pointer)" style="max-height: 30rem;"></b-card-img>
              <b-card-body :overlay="label.url_preview || label.file_pointer">

                <div class="input-group mb-2" v-show="!label.url_preview && !label.file_pointer && edit_labels" style="width: 25rem;">
                  <ChooseVariant
                    @variant="(variant) => updateVariant(label, variant)"
                    :variants="variant_options"
                    :selected="getVariant(label)"
                    :variant-req="true"
                  ></ChooseVariant>
                </div>

                <!-- <div class="input-group mb-2" v-show="!label.url_preview && !label.file_pointer && edit_labels" style="width: 25rem;">
                  <v-select
                    id="product_type"
                    style="width: 25rem;"
                    :options="product_type_options"
                    v-model="label.product_type"
                    label="label"
                    :reduce="option => option.value"
                    area-describedby="product_type-live-feedback"
                    :class="[label.product_type ? '' : 'is-invalid']"
                    v-on:keyup.enter="focus('label_type')"
                  ></v-select>
                  <div id="product_type-live-feedback" class="invalid-feedback">This is a required field.</div>
                </div> -->

                <div class="input-group mb-2" v-show="!label.url_preview && !label.file_pointer && edit_labels" style="width: 25rem;">
                  <v-select
                    id="label_type"
                    style="width: 25rem;"
                    :options="label_type_options"
                    v-model="label.label_type"
                    label="label"
                    :reduce="option => option.value"
                    area-describedby="label_type-live-feedback"
                    :class="[label.label_type ? '' : 'is-invalid']"
                  ></v-select>
                  <div id="label_type-live-feedback" class="invalid-feedback">This is a required field.</div>
                </div>

                <!-- <div class="input-group mb-2" v-show="!label.url_preview && !label.file_pointer && edit_labels" style="width: 25rem;">
                  <input
                    :disabled="!label.product_type"
                    id="qty"
                    type="number"
                    v-model="label.qty"
                    required
                    min="0"
                    aria-describedby="qty-live-feedback"
                    :class="['form-control', (label.qty > 0 ? '' : 'is-invalid')]"
                    v-on:keyup.enter="focus('file')"
                  >
                  <div class="input-group-append">
                    <span v-show="label.product_type === 'capsule'" class="input-group-text">ct</span>
                    <span v-show="label.product_type === 'powder'" class="input-group-text">g</span>
                    <span v-show="label.product_type === 'liquid'" class="input-group-text">ml</span>
                    <span v-show="label.product_type === null" class="input-group-text">?</span>
                  </div>
                  <div id="qty-live-feedback" class="invalid-feedback">This required field must be greater than or equal to zero.</div>
                </div> -->

                <b-form-file :id="'file_'+index" no-drop required accept="image/png, image/jpeg"
                  :disabled="!(!label.url_preview && !label.file_pointer && edit_labels && label.product_type && label.label_type && label.qty)" type="file"
                  v-show="!label.url_preview && !label.file_pointer"
                  class="my-2" @change="onFileChange($event, label)"
                ></b-form-file>
                <div class="d-flex justify-content-between align-items-start flex-column" style="min-height: 100%;min-width: 100%;">
                  <div class="d-flex justify-content-between" style="min-width: 100%;">
                    <div>
                      <b-card v-show="(label.url_preview || label.file_pointer) && label.focus">
                        <b-card-title>V{{ label.label_version }}
                          <b-badge v-if="label.primary" class="ml-3" variant="primary">Primary</b-badge>
                          <b-badge v-show="label.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
                        </b-card-title>
                        <b-card-sub-title>{{ label.date_uploaded }} - {{ label.discontinued ? label.date_discontinued : 'Current' }}</b-card-sub-title>
                        <div>
                          {{ getProductType(label) }} ({{label.qty}}
                            <span v-show="label.product_type === 'capsule'">ct</span>
                            <span v-show="label.product_type === 'powder'">g</span>
                            <span v-show="label.product_type === 'liquid'">ml</span>)<br>
                          {{ getLabelType(label) }}
                        </div>
                      </b-card>
                    </div>
                    <div v-show="(label.url_preview || label.file_pointer) && label.focus && edit_labels">
                      <b-button class="mr-2 mb-2" v-if="!label.primary && !label.discontinued" @click="label.primary = true" variant="primary">Set Primary</b-button>
                      <b-button v-show="!label.primary && !label.discontinued" variant="danger" @click="label.discontinued = true;  label.date_discontinued = new Date().toLocaleDateString('en-US')">Discontinue</b-button>
                    </div>
                  </div>
                  <div>
                    <b-card no-body class="p-1" v-show="(label.url_preview || label.file_pointer) && label.focus && !isTempKey(label.component_id)">
                      <b-button v-on:click.stop variant="light" :to="'/catalogue/components/'+label.component_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
                    </b-card>
                  </div>
                </div>
              </b-card-body>
            </b-card>
            <template #overlay>
              <div class="text-center">
                <h3><b-badge v-show="label.discontinued" variant="danger">Label Discontinued</b-badge></h3>
                <b-form-textarea
                  v-show="!label.primary && label.discontinued"
                  v-model="label.discontinued_reason"
                  :disabled="!edit_labels"
                  class="form-control my-2"
                  placeholder="Reason for Discontinuation"
                ></b-form-textarea>
                <b-button block v-show="!label.primary && label.discontinued && edit_labels" variant="outline-success" @click="label.discontinued = false; label.date_discontinued = null">Reinstate</b-button>
              </div>
            </template>
          </b-overlay>
        </div>
        <div style="max-width: 30rem; min-width: 30rem;" class="m-5" v-show="edit_labels">
          <b-card img-src="../../../assets/no_image_placeholder.png"
            style="cursor: pointer;" v-on:click="newLabel()">
            <b-card-title>New Label</b-card-title>
          </b-card>
        </div>
      </b-card-group>
      <div v-show="edit_labels">
        <b-button class="mr-2" variant="outline-success" @click="submit()">Save</b-button>
        <b-button variant="outline-danger" @click="cancel()">Cancel</b-button>
      </div>
      <div class="d-flex justify-content-center">
        <b-button v-show="show_files" @click="show_files = false" class="m-1" variant="light">Hide Labels</b-button>
      </div>
    </b-collapse>
  </div>
</template>

<script>
import { CustomRequest, genTempKey, isTempKey } from '../../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import labelDoc from './labelDocTemp.js'
import vSelect from 'vue-select'
import ChooseVariant from '../../../components/ChooseVariant.vue'

export default {
  name: 'ProductLabel',
  props: {
    doc: {
      type: Object,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    id: {
      type: Number,
      required: true
    },
    variant_options: {
      required: true,
      type: Array
    },
    timestampFetched: {
      type: String,
      required: true
    }
  },
  components: {
    vSelect,
    ChooseVariant
  },
  data: function () {
    return {
      edit_labels: false,
      edit_labels_buffer: {},
      req: new CustomRequest(this.$cookies.get('session')),
      show_files: false,
      primary_focus: false,
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
      ],
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
      product: {},
      update_components: []
    }
  },
  methods: {
    getVariant: function (label) {
      if (!label.variant_id) {
        return null
      }
      return this.variant_options.find((v) => v.variant_id === label.variant_id)
    },
    updateVariant: function (label, variant) {
      label.variant_id = variant.variant_id
      label.product_type = variant.variant_type
      if (label.product_type === 'powder') {
        label.qty = variant.total_grams_per_unit
      }
      if (label.product_type === 'capsule') {
        label.qty = variant.total_capsules_per_unit
      }
      if (label.product_type === 'liquid') {
        label.qty = variant.total_milliliters_per_unit
      }
      const currentVariant = this.variant_options.find((v) => v.variant_id === variant.variant_id)
      if (currentVariant.discontinued) {
        label.discontinued = true
        label.discontinued_reason = currentVariant.discontinued_reason
      }
    },
    isTempKey: function (key) {
      return isTempKey(key)
    },
    getLabelType: function (l) {
      return this.product_type_options.find((e) => e.value === l.product_type)?.label
    },
    getProductType: function (l) {
      return this.label_type_options.find((e) => e.value === l.label_type)?.label
    },
    focus: function (elmId) {
      document.getElementById(elmId).focus()
    },
    toggleEditLabels: function () {
      this.edit_labels = !this.edit_labels
      this.$emit('editLabels', this.edit_labels)
    },
    setLabelBuffer: function () {
      this.show_files = true
      const labels = cloneDeep(this.doc.labels)
      for (let i = 0; i < labels.all_labels.length; i++) {
        labels.all_labels[i].focus = false
        labels.all_labels[i].primary_focus = false
        labels.all_labels[i].buffered = true
        const currentVariant = this.variant_options.find((v) => v.variant_id === labels.all_labels[i].variant_id)
        if (currentVariant?.discontinued) {
          labels.all_labels[i].discontinued = true
          labels.all_labels[i].discontinued_reason = currentVariant.discontinued_reason
        }
      }
      this.edit_labels_buffer = labels
      this.toggleEditLabels()
    },
    cancel: function () {
      this.edit_labels_buffer = cloneDeep(this.doc.labels)
      this.show_files = false
      this.toggleEditLabels()
    },
    prepareLabelsData: function () {
      const labels = []
      this.edit_labels_buffer.all_labels.forEach(label => {
        const l = {
          file_pointer: label.file_pointer,
          id_code: label.id_code,
          label_version: label.label_version,
          component_id: label.component_id,
          type: label.type,
          discontinued: label.discontinued,
          discontinued_reason: label.discontinued_reason,
          date_discontinued: label.date_discontinued,
          date_uploaded: label.date_uploaded,
          primary: label.primary,
          product_type: label.product_type,
          label_type: label.label_type,
          variant_id: label.variant_id,
          qty: label.qty
        }
        labels.push(l)
        if (isTempKey(l.component_id)) {
          this.createComponent(l)
        }
      })
      const product = {
        doc: {
          labels: {
            date_issued: this.edit_labels_buffer.date_issued,
            date_revised: this.edit_labels_buffer.date_revised,
            notes: this.edit_labels_buffer.notes,
            num_label_versions: this.edit_labels_buffer.num_label_versions,
            num_pouch_versions: this.edit_labels_buffer.num_pouch_versions,
            num_carton_versions: this.edit_labels_buffer.num_carton_versions,
            num_promotional_versions: this.edit_labels_buffer.num_promotional_versions,
            all_labels: cloneDeep(labels)
          },
          specifications: this.doc.specifications,
          formula_files: this.doc.formula_files,
          manufacturing_files: this.doc.manufacturing_files
        },
        product_id: this.id,
        timestamp_fetched: this.timestampFetched
      }
      this.product = product
    },
    createComponentName: function (label) {
      let unit = ''
      if (label.product_type === 'capsule') {
        unit = 'ct'
      } else if (label.product_type === 'powder') {
        unit = 'g'
      } else if (label.product_type === 'liquid') {
        unit = 'ml'
      } else {
        throw new Error('Invalid Product Type')
      }
      return `${this.name} ${label.qty}${unit} (${label.label_type}) Label V${label.label_version}`
    },
    createComponent: function (label) {
      const nameId = genTempKey()
      const componentName = {
        name_id: nameId,
        component_id: label.component_id,
        component_name: this.createComponentName(label),
        primary_name: true,
        botanical_name: false,
        timestamp_fetched: new Date().toISOString()
      }
      const component = {
        component_id: label.component_id,
        component_type: label.label_type,
        certified_fda: this.$parent.product_data.certified_fda,
        certified_gmp: this.$parent.product_data.certified_gmp,
        certified_made_with_organic: this.$parent.product_data.certified_made_with_organic,
        certified_wildcrafted: this.$parent.product_data.certified_wildcrafted,
        certified_usda_organic: this.$parent.product_data.certified_usda_organic,
        certified_halal: this.$parent.product_data.certified_halal,
        certified_kosher: this.$parent.product_data.certified_kosher,
        certified_gluten_free: this.$parent.product_data.certified_gluten_free,
        certified_national_sanitation_foundation: this.$parent.product_data.certified_national_sanitation_foundation,
        certified_us_pharmacopeia: this.$parent.product_data.certified_us_pharmacopeia,
        certified_non_gmo: this.$parent.product_data.certified_non_gmo,
        certified_vegan: this.$parent.product_data.certified_vegan,
        brand_id: this.$parent.product_data.organization_id,
        is_label: true,
        units: 'units',
        doc: this.loadDoc(label),
        timestamp_fetched: new Date().toISOString()
      }
      this.req.upsertRecord('Components', component)
      this.req.upsertRecord('Component_Names', componentName)
      this.req.upsertRecord('Item_id', { component_id: label.component_id, timestamp_fetched: new Date().toISOString() })
      const c = {
        component_id: label.component_id,
        primary_name_id: nameId,
        timestamp_fetched: new Date().toISOString()
      }
      this.update_components.push(c)
    },
    loadDoc: function (label) {
      const doc = labelDoc
      doc.label.url_preview = label.url_preview
      doc.label.file_pointer = label.file_pointer
      doc.label.id_code = label.id_code
      doc.label.label_version = label.label_version
      doc.label.product_id = this.id
      doc.label.type = label.type
      doc.label.date_uploaded = label.date_uploaded
      doc.label.product_type = label.product_type
      doc.label.label_type = label.label_type
      doc.label.qty = label.qty
      return doc
    },
    submit: async function () {
      const createToast = this.$root.createToast
      this.prepareLabelsData()

      // Save Component and Component_Name First.  Get the ids of these new items.
      const resp1 = await this.req.sendRequest(this.$root.getOrigin())
      this.$emit('toggleLoaded', false)

      if (resp1.status !== 201) {
        console.error('Request Error: ', resp1)
        resp1.messages.flash.forEach(message => {
          createToast(message)
        })
        this.$root.handleStaleRequest(this.req.isStale(), window.location)
        return false
      }

      const tempKeyLookup = this.req.getTempKeyLookup()
      const savedFiles = this.req.getSavedFiles()

      this.req = new CustomRequest(this.$cookies.get('session'))

      for (let i = 0; i < this.product.doc.labels.all_labels.length; i++) {
        if (isTempKey(this.product.doc.labels.all_labels[i].component_id)) {
          this.product.doc.labels.all_labels[i].component_id = tempKeyLookup[this.product.doc.labels.all_labels[i].component_id].new_id
          this.product.doc.labels.all_labels[i].file_hash = savedFiles[this.product.doc.labels.all_labels[i].file_pointer].hash
          this.product.doc.labels.all_labels[i].filename = savedFiles[this.product.doc.labels.all_labels[i].file_pointer].filename
          this.product.doc.labels.all_labels[i].page = savedFiles[this.product.doc.labels.all_labels[i].file_pointer].page
          this.product.doc.labels.all_labels[i].ref_count = savedFiles[this.product.doc.labels.all_labels[i].file_pointer].ref_count
          this.product.doc.labels.all_labels[i].filetype = savedFiles[this.product.doc.labels.all_labels[i].file_pointer].filetype
          this.product.doc.labels.all_labels[i].file_pointer = savedFiles[this.product.doc.labels.all_labels[i].file_pointer].file_pointer
        }
      }

      // Save Product with updated labels section.
      this.req.upsertRecord('Product_Master', this.product)

      for (let i = 0; i < this.update_components.length; i++) {
        if (isTempKey(this.update_components[i].component_id)) {
          this.update_components[i].component_id = tempKeyLookup[this.update_components[i].component_id].new_id
          this.update_components[i].primary_name_id = tempKeyLookup[this.update_components[i].primary_name_id].new_id
          this.update_components[i].timestamp_fetched = new Date().toISOString()
          this.req.upsertRecord('Components', this.update_components[i])
        }
      }

      const resp2 = await this.req.sendRequest(this.$root.getOrigin())

      resp2.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp2.status !== 201) {
        console.error('Request Error: ', resp2)
        this.$root.handleStaleRequest(this.req.isStale(), window.location)
        return false
      }

      this.req = new CustomRequest(this.$cookies.get('session'))
      this.edit_labels = false
      this.$parent.edit_labels = false
      this.$parent.getProductData()
      return true
    },
    getFile: function (filename) {
      if (filename) {
        const url = this.$root.getOrigin() + '/api/v1/uploads/' + filename
        return url
      } else {
        return ''
      }
    },
    newLabel: function () {
      if (this.edit_labels_buffer.all_labels.length === 0) {
        this.edit_labels_buffer.date_issued = new Date().toLocaleDateString('en-US')
      }
      const newLabel = {
        url_preview: null,
        file_preview_pointer: null,
        file_pointer: null,
        id_code: null,
        label_version: null,
        component_id: genTempKey(),
        type: null,
        discontinued: false,
        discontinued_reason: '',
        variant_id: null,
        date_discontinued: null,
        date_uploaded: new Date().toLocaleDateString('en-US'),
        focus: false,
        primary: false,
        primary_focus: false,
        product_type: null,
        label_type: null,
        qty: null,
        buffered: false
      }
      this.edit_labels_buffer.all_labels.push(cloneDeep(newLabel))
    },
    setLabelData: function (label) {
      if (label.label_type === 'label') {
        label.label_version = this.edit_labels_buffer.num_label_versions + 1
        label.id_code = `label_${this.name}(${this.id})_label_v(${label.label_version})`
        this.edit_labels_buffer.num_label_versions++
      } else if (label.label_type === 'pouch') {
        label.label_version = this.edit_labels_buffer.num_pouch_versions + 1
        label.id_code = `label_${this.name}(${this.id})_pouch_v(${label.label_version})`
        this.edit_labels_buffer.num_pouch_versions++
      } else if (label.label_type === 'carton') {
        label.label_version = this.edit_labels_buffer.num_carton_versions + 1
        label.id_code = `label_${this.name}(${this.id})_carton_v(${label.label_version})`
        this.edit_labels_buffer.num_carton_versions++
      } else if (label.label_type === 'packaging_material') {
        label.label_version = this.edit_labels_buffer.num_packaging_material_versions + 1
        label.id_code = `label_${this.name}(${this.id})_promo_v(${label.label_version})`
        this.edit_labels_buffer.num_promotional_versions++
      } else {
        label.label_version = null
        label.id_code = null
        return
      }
      this.edit_labels_buffer.date_revised = new Date().toLocaleDateString('en-US')
    },
    onFileChange: async function (e, label) {
      if (e.target.files.length === 0) {
        return
      }

      this.setLabelData(label)

      // Preview File
      const file = e.target.files[0]
      label.url_preview = URL.createObjectURL(file)

      URL.revokeObjectURL(file)

      const customKey = await this.req.addFile(file, 1, label.id_code, 'product_labels')
      label.file_pointer = customKey
      label.buffered = true
    }
  },
  computed: {
    primaryLabels: function () {
      const labels = []
      for (const label of this.edit_labels_buffer.all_labels) {
        if (label.primary) {
          labels.push(label)
        }
      }
      return labels
    }
  },
  created: function () {
    const labels = cloneDeep(this.doc.labels)
    for (let i = 0; i < labels.all_labels.length; i++) {
      labels.all_labels[i].focus = false
      labels.all_labels[i].primary_focus = false
      labels.all_labels[i].buffered = true
      const currentVariant = this.variant_options.find((v) => v.variant_id === labels.all_labels[i].variant_id)
      if (currentVariant?.discontinued) {
        labels.all_labels[i].discontinued = true
        labels.all_labels[i].discontinued_reason = currentVariant.discontinued_reason
      }
    }
    this.edit_labels_buffer = labels
  }
}

</script>

<style scoped>
.vs__dropdown-menu {
  width: 600px;
  max-height: 300px;
  overflow-y: auto;
}

.card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}

.custom-row {
  border-bottom-width: thick !important;
  border-top-width: thick !important;
}
</style>
