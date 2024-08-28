<template>
  <div style="break-inside: avoid;">
    <h3 id="Formulas" class="d-print-none">Formulas<b-button v-if="!edit_formulas && active_tab_index < numVersions" v-b-tooltip.hover title="Edit Product Formulas" @click="set_formula_buffer(false)" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
    <h3 class="d-none d-print-block">Formula</h3>

    <b-tabs content-class="mt-3" v-model="active_tab_index">
      <b-tab v-for="(f, index) in formulas" :key="'index-' + index" :disabled="active_tab_index !== index && edit_formulas">
        <template #title>
          <strong>{{ f.formulation_version+'V' }}<b-badge variant="primary" pill class="ml-2" style="font-size:0.8em;" v-show="f.formula_id === defaultFormulaId">PF</b-badge></strong>
        </template>
        <b-card class="m-2">
          <b-card-title>
            Version {{ f.formulation_version }}
            <b-badge variant="primary" pill class="ml-2" style="font-size:0.8em;" v-show="f.formula_id === defaultFormulaId">Primary Formula</b-badge>
            <b-button v-show="f.formula_id !== defaultFormulaId && !edit_formulas" variant="outline-primary" pill class="ml-2 d-print-none" style="font-size:0.8em;" @click="set_default_formula_id(f.formula_id)">Set as Primary</b-button>
          </b-card-title>
          <b-card-sub-title class="mb-3">{{ new Date(f.timestamp_entered).toLocaleDateString() }} {{ new Date(f.timestamp_entered).toLocaleTimeString() }}</b-card-sub-title>
          <b-card-text>
            <strong v-show="f.notes != null || f.notes?.length > 0">Notes:</strong>
            <b-form-textarea
              v-show="f.notes != null || f.notes?.length > 0"
              v-model="f.notes"
              placeholder="Notes..."
              rows="3"
              max-rows="6"
              id="new-formula-notes"
              class="mb-3"
              :disabled="!edit_formulas"
              @input="update_formula(f)"
            ></b-form-textarea>

            <b-table-lite :items="f['formula_detail']" :fields="fields" striped bordered sticky-header foot-clone head-variant="light" style="min-height: 600px;">
              <template #cell(ingredients_detail)="ingredients_detail">
                <div v-for="(ing, index) in ingredients_detail.value" :key="ing.component_id+'-ingredient'">
                  <b-row align-v="center" class="flex-nowrap">
                    <b-col style="margin: 5px; padding: 0px; margin-left: 10px; max-width: 22px;">
                      <b-badge :id="f.formulation_version+'-'+ingredients_detail.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" v-bind:variant="(ing.priority === 1 ? 'primary' : 'light')" pill class="ml-2">{{ ing.priority }}</b-badge>
                      <b-tooltip :target="f.formulation_version+'-'+ingredients_detail.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" triggers="hover">Priority Level: {{ ing.priority }}</b-tooltip>
                    </b-col>
                    <b-col style="max-width: 260px;"><b-link :to="'/catalogue/components/'+ing.component_id" target="_blank">{{ ing.component_name }}</b-link></b-col>
                    <b-col style="max-width: 360px;"><CertBadge :data="ing"></CertBadge></b-col>
                  </b-row>
                  <hr v-show="index < ingredients_detail.value.length-1">
                </div>
              </template>
              <template #foot(ingredients_detail)=""></template>
              <template #cell(brands)="brands">
                <div v-if="!edit_formulas">
                  <div v-for="(brand) in brands.value" :key="brand.organization_id+'-org'">
                    <b-row align-v="baseline" class="flex-nowrap">
                      <b-col style="margin: 5px; padding: 0px; margin-left: 15px; max-width: 22px;">
                        <b-badge :id="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill>{{ brand.priority }}</b-badge>
                        <b-tooltip :target="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                      </b-col>
                      <b-col>
                        <span :id="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-name'"><b-link :to="'/organizations/'+brand.organization_id" target="_blank">{{ brand.organization_primary_initial }}</b-link></span>
                        <b-tooltip :target="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-name'" triggers="hover">{{ brand.organization_primary_name }}</b-tooltip>
                      </b-col>
                    </b-row>
                  </div>
                </div>
                <div v-else>
                  <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                    <b-row align-v="baseline" class="flex-nowrap">
                      <b-col style="margin: 5px; padding: 0px; margin-left: 15px; max-width: 22px;">
                        <b-badge :id="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(index+1 === 1 ? 'primary' : 'light')" pill class="mr-2">{{ index+1 }}</b-badge>
                        <b-tooltip :target="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ index+1 }}</b-tooltip>
                      </b-col>
                      <b-col style="padding: 0px; margin: 10px; max-width: 48px;;">
                        <b-button @click="remove_brand(brands.item.brands, index)" variant="outline-danger"><b-icon icon="trash"></b-icon></b-button>
                      </b-col>
                      <b-col>
                        <ChooseOrg @org="(o) => select_brand(o, brands.item.brands, index)" :organizations="organization_options" :selected="brand.organization_id === 0 ? null : brand" :org-req="brands.item.specific_brand_required"></ChooseOrg>
                      </b-col>
                    </b-row>
                    <hr v-show="index < brands.value.length">
                  </div>
                  <div class="d-flex justify-content-end">
                    <b-button variant="outline-info" @click="add_brand(brands.item.formula_ingredient_id, brands.item.brands)">Add Brand</b-button>
                  </div>
                </div>
              </template>
              <template #foot(brands)=""></template>
              <template #cell(percent)="percent">
                <strong style="font-size: 1.5em;">{{ percent.value }}%</strong>
              </template>
              <template #foot(percent)="">
                <span :class="calc_total(f['formula_detail']) !== 100 ? 'text-danger':''">= {{ calc_total(f['formula_detail']) }}%</span>
              </template>
              <template #cell(specific_brand_required)="specific_brand_required">
                <div v-if="!edit_formulas">
                  <span v-if="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                  <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
                </div>
                <div v-else>
                  <b-button @click="specific_brand_required.item.specific_brand_required = false;update_row(specific_brand_required.item)" v-show="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                  <b-button @click="specific_brand_required.item.specific_brand_required = true;update_row(specific_brand_required.item)" v-show="!specific_brand_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                </div>
              </template>
              <template #foot(specific_brand_required)=""></template>
              <template #cell(specific_ingredient_required)="specific_ingredient_required">
                <div v-if="!edit_formulas">
                  <span v-if="specific_ingredient_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                  <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
                </div>
                <div v-else>
                  <b-button @click="specific_ingredient_required.item.specific_ingredient_required = false;update_row(specific_ingredient_required.item)" v-show="specific_ingredient_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                  <b-button @click="specific_ingredient_required.item.specific_ingredient_required = true;update_row(specific_ingredient_required.item)" v-show="!specific_ingredient_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                </div>
              </template>
              <template #foot(specific_ingredient_required)=""></template>
              <template #cell(notes)="notes">
                <div v-if="!edit_formulas">{{ notes.value }}</div>
                <b-form-textarea
                  v-else
                  v-model="notes.item.notes"
                  placeholder="Notes..."
                  rows="3"
                  max-rows="6"
                  :id="notes.item.formula_ingredient_id+'-notes'"
                  @input="update_row(notes.item)"
                ></b-form-textarea>
              </template>
              <template #foot(notes)=""></template>
            </b-table-lite>
          </b-card-text>
          <b-button v-show="edit_formulas" class="mr-2" variant="outline-success" @click="save_formula()">Save</b-button>
          <b-button variant="outline-danger" v-show="edit_formulas" @click="cancel()">Cancel</b-button>
        </b-card>
      </b-tab>

      <b-tab title="New Formula" :disabled="active_tab_index < numVersions && edit_formulas" class="d-print-none">
        <b-card class="m-2 d-print-none">
          <b-card-title>New Formula Version {{ numVersions + 1 }}</b-card-title>
          <select id="new_version_selector" class="form-control form-control-lg mb-3" v-model="new_version_select"  @change="set_formula_buffer(true)" :disabled="disable_version_select">
            <option v-for="option in versions" :key="option.value" :value="option.value">{{ option.text }}</option>
          </select>
          <div v-if="disable_version_select && active_tab_index !== numVersions + 1 && edit_formulas">
            <strong>Notes:</strong>
            <b-form-textarea
              v-model="new_formula_buffer.notes"
              placeholder="Notes..."
              rows="3"
              max-rows="6"
              id="new-formula-notes"
              class="mb-3"
              @input="update_formula(new_formula_buffer)"
            ></b-form-textarea>

            <b-table-lite :items="new_formula_buffer.formula_detail" :fields="fields" striped bordered foot-clone sticky-header head-variant="light" style="max-height: 600px;">
              <template #cell(ingredients_detail)="ingredients">
                <div v-for="(ing, index) in ingredients.value" :key="ing.component_id+'-ingredient'">
                  <b-row align-v="baseline" class="flex-nowrap">
                    <b-col style="margin: 5px; padding: 0px; margin-left: 10px; max-width: 22px;">
                      <b-badge :id="(numVersions+1)+'-'+ingredients.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" v-bind:variant="(ing.priority === 1 ? 'primary' : 'light')" pill>{{ ing.priority }}</b-badge>
                      <b-tooltip :target="(numVersions+1)+'-'+ingredients.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" triggers="hover">Priority Level: {{ ing.priority }}</b-tooltip>
                    </b-col>
                    <b-col style="padding: 0px; margin: 10px; max-width: 48px;">
                      <b-button @click="remove_ing(ingredients.item.ingredients_detail, index)" variant="outline-danger"><b-icon icon="trash"></b-icon></b-button>
                    </b-col>
                    <b-col><ChooseIngredient class="py-3" @ing="(i) => select_ing(i, ingredients.item.ingredients_detail, index)" :ingredients="ingredient_options" :selected="ing.component_id === 0 ? null : ing"></ChooseIngredient></b-col>
                  </b-row>
                  <hr v-show="index < ingredients.value.length">
                </div>
                <div class="d-flex justify-content-end">
                  <b-button variant="outline-info" @click="add_ing(ingredients.item.formula_ingredient_id, ingredients.item.ingredients_detail)" class="mr-3">Add Ingredient</b-button>
                  <b-button variant="outline-danger" @click="delete_row(ingredients.index)">Delete Row</b-button>
                </div>
              </template>
              <template #foot(ingredients_detail)=""></template>
              <template #cell(brands)="brands">
                <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                  <b-row align-v="baseline" class="flex-nowrap">
                    <b-col style="margin: 5px; padding: 0px; margin-left: 10px; max-width: 22px;">
                      <b-badge :id="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill>{{ brand.priority }}</b-badge>
                      <b-tooltip :target="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                    </b-col>
                    <b-col style="padding: 0px; margin: 10px; max-width: 48px;;">
                      <b-button @click="remove_brand(brands.item.brands, index)" variant="outline-danger"><b-icon icon="trash"></b-icon></b-button>
                    </b-col>
                    <b-col>
                      <ChooseOrg @org="(o) => select_brand(o, brands.item.brands, index)" :organizations="organization_options" :selected="brand.organization_id === 0 ? null : brand" :org-req="brands.item.specific_brand_required"></ChooseOrg>
                    </b-col>
                  </b-row>
                  <hr v-show="index < brands.value.length">
                </div>
                <div class="d-flex justify-content-end">
                  <b-button variant="outline-info" @click="add_brand(brands.item.formula_ingredient_id, brands.item.brands)">Add Brand</b-button>
                </div>
              </template>
              <template #foot(brands)=""></template>
              <template #cell(percent)="percent">
                <div class="input-group mb-2" style="font-size: 1.5em; width: 80px;">
                  <strong>
                    <input
                    :id="percent.item.formula_ingredient_id+'-percent'"
                    type="number" class="form-control"
                    v-model="percent.item.percent"
                    required
                    min="0"
                    max="100"
                    aria-describedby="percent-live-feedback"
                    :class="['form-control', (percent.item.percent > 0 ? '' : 'is-invalid')]"
                    @input="update_row(percent.item)"
                  >
                  </strong>
                  <div :id="percent.item.formula_ingredient_id+'-percent-live-feedback'" class="invalid-feedback">This required field must be greater than zero.</div>
                </div>
              </template>
              <template #foot(percent)="">
                <span :class="calc_total(new_formula_buffer.formula_detail) !== 100 ? 'text-danger':''">= {{ calc_total(new_formula_buffer.formula_detail) }}%</span>
              </template>
              <template #cell(specific_brand_required)="specific_brand_required">
                <b-button @click="specific_brand_required.item.specific_brand_required = false;update_row(specific_brand_required.item)" v-show="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="specific_brand_required.item.specific_brand_required = true;update_row(specific_brand_required.item)" v-show="!specific_brand_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
              </template>
              <template #foot(specific_brand_required)=""></template>
              <template #cell(specific_ingredient_required)="specific_ingredient_required">
                <b-button @click="specific_ingredient_required.item.specific_ingredient_required = false;update_row(specific_ingredient_required.item)" v-show="specific_ingredient_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="specific_ingredient_required.item.specific_ingredient_required = true;update_row(specific_ingredient_required.item)" v-show="!specific_ingredient_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
              </template>
              <template #foot(specific_ingredient_required)=""></template>
              <template #cell(notes)="notes">
                <b-form-textarea
                  v-model="notes.item.notes"
                  placeholder="Notes..."
                  rows="3"
                  max-rows="6"
                  :id="notes.item.formula_ingredient_id+'-notes'"
                  @input="update_row(notes.item.formula_ingredient_id)"
                ></b-form-textarea>
              </template>
              <template #foot(notes)=""></template>
            </b-table-lite>
          </div>
          <b-button :disabled="!disable_version_select" class="mr-2" variant="outline-success" @click="save_formula()">Save</b-button>
          <b-button :disabled="!disable_version_select" class="mr-2" variant="outline-info" @click="add_row(new_formula_buffer.formula_id)">Add Row</b-button>
          <b-button :disabled="!disable_version_select" variant="outline-danger" @click="cancel()">Cancel</b-button>
        </b-card>
      </b-tab>
    </b-tabs>
    <!-- <b-card v-if="numVersions === 0 && !edit_formulas">
      <b-card-title>No Formulas Exist Yet</b-card-title>
    </b-card> -->
  </div>
</template>

<style scoped>
.hidedropdownarrow {
  -webkit-appearance: none;
  -moz-appearance: none;
  text-indent: 1px;
  text-overflow: '';
}

.card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}

.custom-row {
  border-bottom-width: thick !important;
  border-top-width: thick !important;
}
</style>

<script>
import CertBadge from '../../../components/CertBadge.vue'
import ChooseIngredient from '../../../components/ChooseIngredient.vue'
import ChooseOrg from '../../../components/ChooseOrg.vue'
import { cloneDeep } from 'lodash'
import { CustomRequest, genTempKey, isTempKey } from '../../../common/CustomRequest.js'

export default {
  name: 'ProductFormula',
  components: {
    CertBadge,
    ChooseIngredient,
    ChooseOrg
  },
  props: {
    formulas: {
      type: Array,
      required: true
    },
    defaultFormulaId: {
      required: true
    },
    numVersions: {
      type: Number,
      required: true
    },
    productId: {
      type: Number,
      required: true
    },
    timestampFetched: {
      type: String,
      required: true
    },
    organic: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      edit_formulas: false,
      new_version_select: '',
      disable_version_select: false,
      new_formula_buffer: {},
      fields: [
        { label: 'Ingredient', key: 'ingredients_detail', tdClass: 'custom-row' },
        { label: 'Brands', key: 'brands', tdClass: 'custom-row' },
        { label: '%', key: 'percent', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Brand Specific', key: 'specific_brand_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Cert Specific', key: 'specific_ingredient_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Notes', key: 'notes', tdClass: ['align-middle', 'custom-row'] }
      ],
      versions: [],
      organization_options: [],
      ingredient_options: [],
      new_formula_id: null,
      new_formula_ingredient_id_index: 0,
      active_tab_index: this.formulas.indexOf(this.formulas.find(f => f.formula_id === this.defaultFormulaId)),
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    focus: function (elmId) {
      document.getElementById(elmId).focus()
    },
    set_default_formula_id: function (id) {
      this.$emit('toggleLoaded', false)
      this.req = new CustomRequest(this.$cookies.get('session'))

      const sProduct = {
        product_id: this.productId,
        default_formula_id: id,
        default_formula_version: this.formulas.find(f => f.formula_id === id).formulation_version,
        timestamp_fetched: this.timestampFetched
      }
      this.req.upsertRecord('Product_Master', sProduct)

      this.req.sendRequest(window.origin).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status === 201) {
          this.cancel()
          this.$nextTick(() => {
            this.versions = []
            this.build_formula_versions()
          })
          this.$parent.getProductData()
        }
        this.$root.handleStaleRequest(this.req.isStale(), window.location)
      })
    },
    update_formula: function (formula) {
      const update = {
        formula_id: formula.formula_id,
        notes: formula.notes,
        product_id: this.productId,
        timestamp_fetched: formula.timestamp_fetched
      }
      this.req.updateUpsertRecord('Formula_Master', 'formula_id', formula.formula_id, update)
    },
    validate_new_formula_buffer: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Formula',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }
      const createToast = this.$root.createToast

      // Check Validations
      let valid = true

      // Formula Percent
      let total = 0
      for (const f in this.new_formula_buffer.formula_detail) {
        total += this.new_formula_buffer.formula_detail[f].percent
        if (this.new_formula_buffer.formula_detail[f].percent === 0) {
          errorToast.message = 'Formula Percent cannot be zero.'
          createToast(errorToast)
          valid = false
          break
        }
      }
      if (Math.round(total * 100) / 100 !== 100) {
        errorToast.message = 'Formula Percent must equal 100% exactly.'
        createToast(errorToast)
        valid = false
      }

      // Check valid Ingredients
      for (const f in this.new_formula_buffer.formula_detail) {
        if (this.new_formula_buffer.formula_detail[f].ingredients_detail.length === 0) {
          errorToast.message = 'All rows must have at least one ingredient selected.'
          createToast(errorToast)
          valid = false
          break
        }
        for (const i in this.new_formula_buffer.formula_detail[f].ingredients_detail) {
          if (!this.new_formula_buffer.formula_detail[f].ingredients_detail[i].component_id > 0) {
            errorToast.message = 'Invalid ingredients selected.'
            createToast(errorToast)
            valid = false
            break
          }
        }
      }

      // Check valid Brands
      for (const f in this.new_formula_buffer.formula_detail) {
        if (!this.new_formula_buffer.formula_detail[f].brands.length > 0 && this.new_formula_buffer.formula_detail[f].specific_brand_required) {
          errorToast.message = 'All rows requiring brand specific ingredients must have at least one brand selected.'
          createToast(errorToast)
          valid = false
          break
        }
        for (const i in this.new_formula_buffer.formula_detail[f].brands) {
          if (!this.new_formula_buffer.formula_detail[f].brands[i].organization_id > 0) {
            errorToast.message = 'Invalid brands selected.'
            createToast(errorToast)
            valid = false
            break
          }
        }
      }

      return valid
    },
    save_formula: function () {
      // Check valid formula
      this.$emit('toggleLoaded', false)
      if (!this.validate_new_formula_buffer()) {
        this.$emit('toggleLoaded', true)
        return
      }

      if (this.new_version_select !== '' || this.new_version_select === 'NEW') {
        const updateProduct = {
          product_id: this.productId,
          num_formula_versions: this.numVersions + 1,
          timestamp_fetched: this.timestampFetched
        }
        // if (this.numVersions + 1 === 1) {
        //   updateProduct.default_formula_version = this.new_formula_id
        // }
        this.req.upsertRecord('Product_Master', updateProduct)
      }

      this.req.sendRequest(window.origin).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status === 201) {
          this.cancel()
          this.$parent.getProductData()
          this.versions = []
          this.build_formula_versions()
        } else {
          this.$root.handleStaleRequest(this.req.isStale(), window.location)
          this.$parent.toggleLoaded(true)
        }
      })
    },
    toggle_edit_formulas: function () {
      this.edit_formulas = !this.edit_formulas
      this.$emit('editFormulas', this.edit_formulas)
    },
    cancel: function () {
      this.$emit('toggleLoaded', false)
      this.$emit('refreshParent')
      this.disable_version_select = false
      this.new_version_select = ''
      this.new_formula_buffer = {}
      this.req = new CustomRequest(this.$cookies.get('session'))
      this.$nextTick(() => {
        this.toggle_edit_formulas()
      })
    },
    calc_total: function (formulaDetail) {
      let total = 0
      for (const f in formulaDetail) {
        total += formulaDetail[f].percent
      }
      return Math.round(total * 100) / 100
    },
    remove_brand: function (brands, index) {
      const brand = brands.splice(index, 1)[0]
      if (isTempKey(brand._id)) {
        this.req.removeUpsertRecord('Ingredient_Brands_Join', '_id', brand._id)
      } else {
        this.req.updateDeleteRecord('Ingredient_Brands_Join', '_id', brand._id, { _id: brand._id })
      }
      for (let i = index; i < brands.length; i++) {
        brands[i].priority = i + 1
        const b = {
          _id: brands[i]._id,
          brand_id: brands[i].organization_id,
          priority: brands[i].priority,
          formula_ingredient_id: brands[i].formula_ingredient_id,
          timestamp_fetched: brands[i].timestamp_fetched
        }
        if (isTempKey(brand._id)) {
          this.req.updateUpsertRecord('Ingredient_Brands_Join', '_id', brands[i]._id, b)
        } else {
          this.req.upsertRecord('Ingredient_Brands_Join', b)
        }
      }
      const formulaDetailUpdate = {
        formula_ingredient_id: brand.formula_ingredient_id,
        num_brands: brands.length,
        timestamp_fetched: this.timestampFetched
      }
      this.req.updateUpsertRecord('Formula_Detail', 'formula_ingredient_id', brand.formula_ingredient_id, formulaDetailUpdate)
    },
    add_brand: function (formulaIngredientId, brands) {
      const brand = {
        _id: genTempKey(),
        priority: brands.length + 1,
        formula_ingredient_id: formulaIngredientId,
        organization_id: null,
        organization_primary_name: null,
        organization_primary_initial: null,
        timestamp_fetched: new Date().toISOString()
      }
      brands.push(brand)
    },
    select_brand: function (org, brands, index) {
      const priority = brands[index].priority
      if (org !== null) {
        const brand = {
          _id: brands[index]._id,
          brand_id: brands[index].organization_id,
          priority: brands[index].priority,
          formula_ingredient_id: brands[index].formula_ingredient_id,
          timestamp_fetched: brands[index].timestamp_fetched
        }
        brands[index] = org
        brands[index].priority = priority
        brands[index]._id = brand._id
        brands[index].brand_id = org.organization_id
        brands[index].priority = priority
        brands[index].formula_ingredient_id = brand.formula_ingredient_id
        brands[index].timestamp_fetched = brand.timestamp_fetched
        this.req.updateUpsertRecord('Ingredient_Brands_Join', '_id', brand._id, brand)
      }
      const formulaDetailUpdate = {
        formula_ingredient_id: brands[index].formula_ingredient_id,
        num_brands: brands.length,
        timestamp_fetched: this.timestampFetched
      }
      this.req.updateUpsertRecord('Formula_Detail', 'formula_ingredient_id', brands[index].formula_ingredient_id, formulaDetailUpdate)
    },
    remove_ing: function (ingredientsDetail, index) {
      const ingDet = ingredientsDetail.splice(index, 1)[0]
      if (isTempKey(ingDet._id)) {
        this.req.removeUpsertRecord('Ingredients_Join', '_id', ingDet._id)
      } else {
        this.req.updateDeleteRecord('Ingredients_Join', '_id', ingDet._id, { _id: ingDet._id })
      }
      for (let i = index; i < ingredientsDetail.length; i++) {
        ingredientsDetail[i].priority = i + 1
        const ing = {
          _id: ingredientsDetail[i]._id,
          ingredient_id: ingredientsDetail[i].component_id,
          priority: ingredientsDetail[i].priority,
          formula_ingredient_id: ingredientsDetail[i].formula_ingredient_id,
          timestamp_fetched: ingredientsDetail[i].timestamp_fetched
        }
        if (isTempKey(ingDet._id)) {
          this.req.updateUpsertRecord('Ingredients_Join', '_id', ingredientsDetail[i]._id, ing)
        } else {
          this.req.upsertRecord('Ingredients_Join', ing)
        }
      }
      const formulaDetailUpdate = {
        formula_ingredient_id: ingredientsDetail[index].formula_ingredient_id,
        num_ingredients: ingredientsDetail.length,
        timestamp_fetched: this.timestampFetched
      }
      this.req.updateUpsertRecord('Formula_Detail', 'formula_ingredient_id', ingredientsDetail[index].formula_ingredient_id, formulaDetailUpdate)
    },
    add_ing: function (formulaIngredientId, ingredientsDetail) {
      const ing = {
        _id: genTempKey(),
        component_id: null,
        priority: ingredientsDetail.length + 1,
        formula_ingredient_id: formulaIngredientId,
        component_name: null,
        component_primary_name: null,
        timestamp_fetched: new Date().toISOString()
      }
      ingredientsDetail.push(ing)
    },
    select_ing: function (ing, ingredients, index) {
      const priority = ingredients[index].priority
      if (ing !== null) {
        const ingredient = {
          _id: ingredients[index]._id,
          ingredient_id: ingredients[index].component_id,
          priority: ingredients[index].priority,
          formula_ingredient_id: ingredients[index].formula_ingredient_id,
          timestamp_fetched: ingredients[index].timestamp_fetched
        }
        ingredients[index] = ing
        ingredients[index].priority = priority
        ingredients[index]._id = ingredient._id
        ingredients[index].component_id = ing.component_id
        ingredients[index].priority = priority
        ingredients[index].formula_ingredient_id = ingredient.formula_ingredient_id
        ingredients[index].timestamp_fetched = ingredient.timestamp_fetched
        this.req.updateUpsertRecord('Ingredients_Join', '_id', ingredient._id, ingredient)
        const formulaDetailUpdate = {
          formula_ingredient_id: ingredients[index].formula_ingredient_id,
          num_ingredients: ingredients.length,
          timestamp_fetched: this.timestampFetched
        }
        this.req.updateUpsertRecord('Formula_Detail', 'formula_ingredient_id', ingredients[index].formula_ingredient_id, formulaDetailUpdate)
      }
    },
    delete_row: function (index) {
      const row = this.new_formula_buffer.formula_detail.splice(index, 1)
      row.brands.forEach(brand => {
        if (isTempKey(brand._id)) {
          this.req.removeUpsertRecord('Ingredient_Brands_Join', '_id', brand._id)
        } else {
          this.req.deleteRecord('Ingredient_Brands_Join', { _id: brand._id })
        }
      })
      row.ingredients_detail.forEach(ing => {
        if (isTempKey(ing._id)) {
          this.req.removeUpsertRecord('Ingredients_Join', '_id', ing._id)
        } else {
          this.req.deleteRecord('Ingredients_Join', { _id: ing._id })
        }
      })
      if (isTempKey(row.formula_ingredient_id)) {
        this.req.removeUpsertRecord('Formula_Detail', 'formula_ingredient_id', row.formula_ingredient_id)
      } else {
        this.req.deleteRecord('Formula_Detail', { formula_ingredient_id: row.formula_ingredient_id })
      }
    },
    update_row: function (row) {
      const id = row.formula_ingredient_id
      const updateRowBuffer = {
        formula_id: row.formula_id,
        formula_ingredient_id: id,
        notes: row.notes,
        percent: row.percent,
        specific_brand_required: row.specific_brand_required,
        specific_ingredient_required: row.specific_ingredient_required,
        timestamp_fetched: row.timestamp_fetched
      }
      this.req.updateUpsertRecord('Formula_Detail', 'formula_ingredient_id', id, updateRowBuffer)
    },
    add_row: function (formulaId) {
      const formulaIngredientId = genTempKey()
      const rowBuffer = {
        brands: [],
        formula_id: formulaId,
        formula_ingredient_id: formulaIngredientId,
        ingredients_detail: [
          {
            _id: genTempKey(),
            ingredient_id: null,
            component_id: null,
            priority: 1,
            formula_ingredient_id: formulaIngredientId,
            timestamp_fetched: new Date().toISOString()
          }
        ],
        notes: null,
        percent: 0,
        specific_brand_required: false,
        specific_ingredient_required: false,
        timestamp_fetched: new Date().toISOString()
      }
      this.new_formula_ingredient_id_index++
      this.new_formula_buffer.formula_detail.push(rowBuffer)
      const row = {
        formula_ingredient_id: formulaIngredientId,
        formula_id: formulaId,
        notes: null,
        percent: 0,
        specific_brand_required: false,
        specific_ingredient_required: false,
        timestamp_fetched: new Date().toISOString()
      }
      this.req.upsertRecord('Formula_Detail', row)
    },
    set_formula_buffer: function (selector) {
      this.$emit('toggleLoaded', false)
      this.req = new CustomRequest(this.$cookies.get('session'))

      let buffer = {}
      buffer.formulation_version = this.numVersions + 1
      buffer.formula_id = this.new_formula_id
      buffer.product_id = this.productId
      buffer.notes = ''
      buffer.timestamp_fetched = new Date().toISOString()
      buffer.formula_detail = []

      const newFormula = {
        formula_id: this.new_formula_id,
        formulation_version: this.numVersions + 1,
        product_id: this.productId,
        notes: '',
        timestamp_fetched: new Date().toISOString()
      }

      this.req.upsertRecord('Formula_Master', newFormula)

      if (selector && this.new_version_select !== 'NEW') {
        const copy = cloneDeep(this.formulas.find(f => f.formulation_version === this.new_version_select))

        buffer.notes = copy.notes

        copy.formula_detail.forEach((f, i) => {
          const k = genTempKey()
          f.formula_ingredient_id = k
          const row = {
            formula_ingredient_id: k,
            formula_id: this.new_formula_id,
            notes: f.notes,
            percent: f.percent,
            specific_brand_required: f.specific_brand_required,
            specific_ingredient_required: f.specific_ingredient_required,
            timestamp_fetched: new Date().toISOString(),
            num_brands: f.brands.length,
            num_ingredients: f.ingredients_detail.length
          }
          this.req.upsertRecord('Formula_Detail', row)
          buffer.formula_detail.push({ ...f, ...row })
          f.ingredients_detail.forEach((ing, j) => {
            const newIng = {
              _id: genTempKey(),
              ingredient_id: ing.ingredient_id ? ing.ingredient_id : ing.component_id,
              priority: ing.priority,
              formula_ingredient_id: k,
              timestamp_fetched: new Date().toISOString()
            }
            this.req.updateUpsertRecord('Ingredients_Join', '_id', newIng._id, newIng)
            buffer.formula_detail[i].ingredients_detail[j] = { ...ing, ...newIng }
          })
          f.brands.forEach((b, j) => {
            const newBrand = {
              _id: genTempKey(),
              brand_id: b.brand_id ? b.brand_id : b.organization_id,
              priority: b.priority,
              formula_ingredient_id: k,
              timestamp_fetched: new Date().toISOString()
            }
            this.req.updateUpsertRecord('Ingredient_Brands_Join', '_id', newBrand._id, newBrand)
            buffer.formula_detail[i].brands[j] = { ...b, ...newBrand }
          })
        })
      } else if (this.new_version_select !== 'NEW') {
        buffer = this.formulas[this.active_tab_index]
      }

      this.disable_version_select = true
      this.edit_formulas = true
      this.new_formula_buffer = cloneDeep(buffer)
      this.$parent.edit_formulas = true
      this.edit_formulas = true
      this.$parent.toggleLoaded(true)
    },
    build_formula_versions: function () {
      for (const f in this.formulas) {
        this.versions.push({ value: this.formulas[f].formulation_version, text: 'Copy V' + this.formulas[f].formulation_version + (this.formulas[f].formula_id === this.defaultFormulaId ? ' (PRIMARY)' : '') })
      }
      this.versions.push({ value: 'NEW', text: 'New Formula' })
    },
    get_organizations: function () {
      const fetchRequest = window.origin + '/api/v1/organizations'
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
            const orgs = Object.values(data.data)
            this.organization_options = orgs.sort((a, b) => {
              return a?.organization_primary_name > b?.organization_primary_name ? 1 : -1
            })
            // eslint-disable-next-line
            console.log(this.organization_options)
            if (this.organization_options.doc === null) {
              this.organization_options.doc = {}
            }
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
    },
    get_ingredients: function () {
      let fetchRequest = window.origin + '/api/v1/catalogue/components?type=powder&populdate=component_names'
      if (this.organic) {
        fetchRequest += '&certification=usda_organic'
      }
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
            const ings = Object.values(data.data)
            this.ingredient_options = ings.sort((a, b) => (a.component_primary_name > b.component_name ? 1 : -1))
            // eslint-disable-next-line
            console.log(this.ingredient_options)
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
  watch: {
    new_version_select: function () {
      this.toggle_edit_formulas()
    }
  },
  created: function () {
    this.new_formula_id = genTempKey()
    this.build_formula_versions()
    this.get_organizations()
    this.get_ingredients()
  }
}
</script>
