<template>
  <div>
    <h3 id="ProductVariants">Product Variants<b-button v-if="!edit_variants" v-b-tooltip.hover title="Edit Product Variants" @click="toggle_edit_variants()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>

    <b-card-group deck class="mb-3">
      <div v-for="variant in variants_buffer" :key="variant.variant_id">
        <b-overlay :show="variant.discontinued" :opacity="0.50" rounded="sm">
          <b-card>
            <b-card-title class="d-flex justify-content-between">
              <span v-if="variant.variant_type === 'powder'">Powder Fill - {{ (variant?.total_grams_per_unit ? variant.total_grams_per_unit : 0) + 'g' }} {{ variant?.variant_title_suffix ? variant.variant_title_suffix : '' }}</span>
              <span v-if="variant.variant_type === 'liquid'">Liquid Fill - {{ (variant?.total_milliliters_per_unit ? variant.total_milliliters_per_unit : 0) + 'ml' }} {{ variant?.variant_title_suffix ? variant.variant_title_suffix : '' }}</span>
              <span v-if="variant.variant_type === 'capsule'">Capsule Fill - {{ (variant?.total_capsules_per_unit ? variant.total_capsules_per_unit : 0) + 'ct' }} {{ variant?.variant_title_suffix ? variant.variant_title_suffix : '' }}</span>
              <b-badge v-show="variant.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
              <b-badge v-show="variant.primary_variant && !edit_variants" class="ml-3" variant="primary">Primary</b-badge>
            </b-card-title>
            <b-card-text>
              <div v-if="edit_variants">
                <b-button block v-show="!variant.primary_variant" variant="outline-primary" @click="variant.primary_variant = true; update_variant(variant)" class="mb-3">Primary</b-button>
                <b-button block v-show="variant.primary_variant" variant="primary" @click="variant.primary_variant = false; update_variant(variant)" class="mb-3">Primary</b-button>
              </div>
              <div v-if="edit_variants">
                <b-row>
                  <b-col><label for="max_grams_per_unit"><strong>Variant Title:</strong></label></b-col>
                  <b-col>
                    <div role="group" class="input-group mb-2">
                      <div class="input-group-prepend">
                        <div class="input-group-text">
                          {{ variant.variant_type === 'powder' ? (variant?.total_grams_per_unit ? variant.total_grams_per_unit : 0) + 'g' : '' }}
                          {{ variant.variant_type === 'liquid' ? (variant?.total_milliliters_per_unit ? variant.total_milliliters_per_unit : 0) + 'ml' : '' }}
                          {{ variant.variant_type === 'capsule' ? (variant?.total_capsules_per_unit ? variant.total_capsules_per_unit : 0) + 'ct' : '' }}
                        </div>
                      </div>
                      <input
                        :id="'variant_title_suffix'+variant.variant_id"
                        type="text"
                        v-model="variant.variant_title_suffix"
                        :disabled="!edit_variants"
                        @input="update_variant(variant)"
                        class="form-control"
                      >
                    </div>
                  </b-col>
                </b-row>
              </div>
              <div>
                <b-row>
                  <b-col><label for="notes"><strong>Notes:</strong></label></b-col>
                </b-row>
                <b-row>
                  <b-col>
                    <b-form-textarea
                      id="notes"
                      v-model="variant.notes"
                      :disabled="!edit_variants"
                      @input="update_variant(variant)"
                      class="form-control"
                    ></b-form-textarea>
                  </b-col>
                </b-row>
                <hr>
              </div>
              <div v-if="variant.variant_type === 'powder'">
                <b-row>
                  <b-col><label for="max_grams_per_unit"><strong>Tolerance Max:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'max_grams_per_unit'+variant.variant_id"
                        type="number"
                        v-model="variant.max_grams_per_unit"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="max_grams_per_unit-live-feedback"
                        :class="['form-control', (variant.max_grams_per_unit >= variant.total_grams_per_unit && variant.max_grams_per_unit !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('total_grams_per_unit'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">g</span>
                      </div>
                      <div id="max_grams_per_unit-live-feedback" class="invalid-feedback">This required field must be greater than or equal to the target.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col><label for="total_grams_per_unit"><strong>Target g per Product:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'total_grams_per_unit'+variant.variant_id"
                        type="number"
                        class="form-control"
                        v-model="variant.total_grams_per_unit"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="total_grams_per_unit-live-feedback"
                        :class="['form-control', (variant.total_grams_per_unit >= 0 && variant.total_grams_per_unit !== '' && variant.total_grams_per_unit !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('min_grams_per_unit'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">g</span>
                      </div>
                      <div id="total_grams_per_unit-live-feedback" class="invalid-feedback">This is a required field.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col><label for="min_grams_per_unit"><strong>Tolerance Min:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'min_grams_per_unit'+variant.variant_id"
                        type="number"
                        v-model="variant.min_grams_per_unit"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="min_grams_per_unit-live-feedback"
                        :class="['form-control', (variant.min_grams_per_unit <= variant.total_grams_per_unit && variant.min_grams_per_unit !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('max_grams_per_unit'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">g</span>
                      </div>
                      <div id="min_grams_per_unit-live-feedback" class="invalid-feedback">This required field must be less than or equal to the target.</div>
                    </div>
                  </b-col>
                </b-row>
              </div>
              <div v-if="variant.variant_type === 'liquid'">
                <b-row>
                  <b-col><label for="max_milliliters_per_unit"><strong>Tolerance Max:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'max_milliliters_per_unit'+variant.variant_id"
                        type="number"
                        v-model="variant.max_milliliters_per_unit"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="max_milliliters_per_unit-live-feedback"
                        :class="['form-control', (variant.max_milliliters_per_unit >= variant.total_milliliters_per_unit && variant.max_milliliters_per_unit !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('total_milliliters_per_unit'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">ml</span>
                      </div>
                      <div id="max_milliliters_per_unit-live-feedback" class="invalid-feedback">This required field must be greater than or equal to the target.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col><label for="total_milliliters_per_unit"><strong>Target ml per Product:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'total_milliliters_per_unit'+variant.variant_id"
                        type="number"
                        v-model="variant.total_milliliters_per_unit"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="total_milliliters_per_unit-live-feedback"
                        :class="['form-control', (variant.total_milliliters_per_unit >= 0 && variant.total_milliliters_per_unit !== '' && variant.total_milliliters_per_unit !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('min_milliliters_per_unit'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">ml</span>
                      </div>
                      <div id="total_milliliters_per_unit-live-feedback" class="invalid-feedback">This is a required field.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col><label for="min_milliliters_per_unit"><strong>Tolerance Min:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'min_milliliters_per_unit'+variant.variant_id"
                        type="number"
                        v-model="variant.min_milliliters_per_unit"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="min_milliliters_per_unit-live-feedback"
                        :class="['form-control', (variant.min_milliliters_per_unit <= variant.total_milliliters_per_unit && variant.min_milliliters_per_unit !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('max_milliliters_per_unit'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">ml</span>
                      </div>
                      <div id="min_milliliters_per_unit-live-feedback" class="invalid-feedback">This required field must be less than or equal to the target.</div>
                    </div>
                  </b-col>
                </b-row>
              </div>
              <div v-if="variant.variant_type === 'capsule'">
                <b-row>
                  <b-col><label for="max_mg_per_capsule"><strong>Tolerance Max:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'max_mg_per_capsule'+variant.variant_id"
                        type="number"
                        v-model="variant.max_mg_per_capsule"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="max_mg_per_capsule-live-feedback"
                        :class="['form-control', (variant.max_mg_per_capsule >= variant.total_mg_per_capsule && variant.max_mg_per_capsule !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('total_mg_per_capsule'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">mg</span>
                      </div>
                      <div id="max_mg_per_capsule-live-feedback" class="invalid-feedback">This required field must be greater than or equal to the target.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col><label for="total_mg_per_capsule"><strong>Target mg per Product:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'total_mg_per_capsule'+variant.variant_id"
                        type="number"
                        v-model="variant.total_mg_per_capsule"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="total_mg_per_capsule-live-feedback"
                        :class="['form-control', (variant.total_mg_per_capsule !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('min_mg_per_capsule'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">mg</span>
                      </div>
                      <div id="total_mg_per_capsule-live-feedback" class="invalid-feedback">This is a required field.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row>
                  <b-col><label for="min_mg_per_capsule"><strong>Tolerance Min:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        :id="'min_mg_per_capsule'+variant.variant_id"
                        type="number"
                        v-model="variant.min_mg_per_capsule"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="min_mg_per_capsule-live-feedback"
                        :class="['form-control', (variant.total_mg_per_capsule >= variant.min_mg_per_capsule && variant.min_mg_per_capsule !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                        v-on:keyup.enter="focus('max_mg_per_capsule'+variant.variant_id)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">mg</span>
                      </div>
                      <div id="min_mg_per_capsule-live-feedback" class="invalid-feedback">This required field must be less than or equal to the target.</div>
                    </div>
                  </b-col>
                </b-row>
                <hr>
                <b-row>
                  <b-col><label for="total_capsules_per_unit"><strong>Capsule Count:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        id="total_capsules_per_unit"
                        type="number"
                        v-model="variant.total_capsules_per_unit"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="total_capsules_per_unit-live-feedback"
                        :class="['form-control', (variant.total_capsules_per_unit >= 0 && variant.total_capsules_per_unit !== '' && variant.total_capsules_per_unit !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">ct</span>
                      </div>
                      <div id="total_capsules_per_unit-live-feedback" class="invalid-feedback">This required field must be greater than or equal to zero.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row class="mb-2">
                  <b-col><label for="capsule_size"><strong>Capsule Size:</strong></label></b-col>
                  <b-col>
                    <select
                      id="capsule_size"
                      v-model="variant.capsule_size"
                      :disabled="!edit_variants"
                      aria-describedby="capsule_size-live-feedback"
                      :class="['form-control', 'form-control-md', (variant.capsule_size !== '' ? '' : 'is-invalid'), 'custom-select']"
                      @change="update_variant(variant)"
                    >
                      <option selected value="">Select Size</option>
                      <option value="n/a">N/A</option>
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="0">0</option>
                      <option value="00">00</option>
                  </select>
                  <div id="capsule_size-live-feedback" class="invalid-feedback">This is a required field.</div>
                </b-col>
                </b-row>
                <b-row>
                  <b-col><label for="mg_empty_capsule"><strong>Capsule Weight:</strong></label></b-col>
                  <b-col>
                    <div class="input-group mb-2">
                      <input
                        id="mg_empty_capsule"
                        type="number"
                        v-model="variant.mg_empty_capsule"
                        required
                        min="0"
                        :disabled="!edit_variants"
                        aria-describedby="mg_empty_capsule-live-feedback"
                        :class="['form-control', (variant.mg_empty_capsule >= 0 && variant.mg_empty_capsule !== '' && variant.mg_empty_capsule !== null ? '' : 'is-invalid')]"
                        @input="update_variant(variant)"
                      >
                      <div class="input-group-append">
                        <span class="input-group-text">mg</span>
                      </div>
                      <div id="mg_empty_capsule-live-feedback" class="invalid-feedback">This required field must be greater than or equal to zero.</div>
                    </div>
                  </b-col>
                </b-row>
              </div>
              <div v-if="edit_variants">
                <hr>
                <b-row v-if="isTempKey(variant.variant_id)">
                  <b-col>
                    <b-button variant="outline-danger" @click="delete_temp_variant(variant)">Delete</b-button>
                  </b-col>
                </b-row>
                <div v-else>
                  <b-row>
                    <b-col><label :for="'discontinued_reason'+variant.variant_id"><strong>Discontinue Variant:</strong></label></b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <b-form-textarea
                        v-model="variant.discontinued_reason"
                        :disabled="!edit_variants"
                        @input="update_variant(variant)"
                        class="form-control"
                      ></b-form-textarea>
                    </b-col>
                  </b-row>
                  <b-button block class="mt-3" v-show="!variant.discontinued" :disabled="!variant.discontinued_reason" variant="outline-danger" @click="discontinue_variant(variant, variant.discontinued_reason)">Discontinue</b-button>
                </div>
              </div>
            </b-card-text>
          </b-card>
          <template #overlay>
            <b-card class="d-flex align-content-end mx-6">
              <div class="text-center">
                <h2><b-badge v-show="variant.discontinued" variant="danger">Variant Discontinued</b-badge></h2>
                <b-form-textarea
                  v-model="variant.discontinued_reason"
                  disabled
                  class="form-control"
                ></b-form-textarea>
                <b-button block class="mt-3" v-show="variant.discontinued && edit_variants" :disabled="!variant.discontinued_reason" variant="outline-success" @click="reinstate_variant(variant)">Reinstate</b-button>
              </div>
            </b-card>
          </template>
        </b-overlay>
      </div>
      <b-card v-show="new_variant.variant_type !== undefined" style="width: 508px;">
        <b-card-title>New Variant</b-card-title>
        <b-card-text>
          <h5>Select Variant Type</h5>
          <select
            id="variant_type"
            v-model="new_variant.variant_type"
            aria-describedby="variant_type-live-feedback"
            :class="['form-control', 'form-control-md', (!!new_variant.variant_type ? '' : 'is-invalid')]"
            v-on:keyup.enter="focus('mg_empty_capsule')"
          >
            <option value="powder">Powder Fill</option>
            <option value="capsule">Capsule Fill</option>
            <option value="liquid">Liquid Fill</option>
          </select>
          <div id="variant_type-live-feedback" class="invalid-feedback">This is a required field.</div>
          <b-button block class="mt-3" variant="outline-success" @click="buffer_new_variant()">Next</b-button>
        </b-card-text>
      </b-card>
      <div v-show="variants_buffer.length === 0 && !edit_variants">
        <b-card style="max-width: 100%;">
          <b-card-title>No Product Variants</b-card-title>
          <b-card-text>
            <h5>There are no variants for this product.</h5>
          </b-card-text>
        </b-card>
      </div>
    </b-card-group>

    <div v-show="edit_variants">
      <b-button class="mr-2" variant="outline-success" :disabled="new_variant?.variant_type === null || variants_buffer.length === 0" @click="save_variants()">Save</b-button>
      <b-button class="mr-2" variant="outline-info" :disabled="new_variant?.variant_type === null" @click="add_variant()">New Variant</b-button>
      <b-button variant="outline-danger" @click="cancel()">Cancel</b-button>
    </div>

  </div>
</template>

<script>
import { cloneDeep } from 'lodash'
import { CustomRequest, genTempKey, isTempKey } from '../../../common/CustomRequest.js'

export default {
  name: 'ProductVariant',
  props: {
    productVariants: {
      type: Array,
      required: true
    },
    numVariants: {
      type: Number,
      required: true
    },
    productId: {
      type: Number,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      edit_variants: false,
      variants_buffer: [],
      num_variants: 0,
      new_variant: {},
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    isTempKey: function (key) {
      return isTempKey(key)
    },
    focus: function (elmId) {
      document.getElementById(elmId).focus()
    },
    buffer_new_variant: function () {
      this.variants_buffer.unshift(cloneDeep(this.new_variant))
      this.update_variant(this.new_variant)
      this.new_variant = {}
      this.num_variants += 1
    },
    get_variant_title: function (variant) {
      if (variant.variant_type === 'powder') {
        return `${variant.total_grams_per_unit}g ${(variant.variant_title_suffix ? variant.variant_title_suffix : '')}`
      }
      if (variant.variant_type === 'liquid') {
        return `${variant.total_milliliters_per_unit}ml ${(variant.variant_title_suffix ? variant.variant_title_suffix : '')}`
      }
      if (variant.variant_type === 'capsule') {
        return `${variant.total_capsules_per_unit}ct ${(variant.variant_title_suffix ? variant.variant_title_suffix : '')}`
      }
      return 'ERROR TITLE'
    },
    update_variant: function (variant) {
      const title = this.get_variant_title(variant)
      const update = {
        variant_id: variant.variant_id,
        product_id: this.productId,
        variant_title: title,
        variant_title_suffix: variant.variant_title_suffix,
        variant_type: variant.variant_type,
        primary_variant: variant.primary_variant,
        discontinued: variant.discontinued,
        discontinued_reason: variant.discontinued_reason,
        notes: variant.notes,
        min_grams_per_unit: variant.min_grams_per_unit,
        total_grams_per_unit: variant.total_grams_per_unit,
        max_grams_per_unit: variant.max_grams_per_unit,
        min_milliliters_per_unit: variant.min_milliliters_per_unit,
        total_milliliters_per_unit: variant.total_milliliters_per_unit,
        max_milliliters_per_unit: variant.max_milliliters_per_unit,
        min_mg_per_capsule: variant.min_mg_per_capsule,
        total_mg_per_capsule: variant.total_mg_per_capsule,
        max_mg_per_capsule: variant.max_mg_per_capsule,
        total_capsules_per_unit: variant.total_capsules_per_unit,
        capsule_size: variant.capsule_size,
        mg_empty_capsule: variant.mg_empty_capsule
      }
      const index = this.variants_buffer.indexOf(variant)
      this.variants_buffer[index] = { ...this.variants_buffer[index], ...update }
      this.req.updateUpsertRecord('Product_Variant', 'variant_id', variant.variant_id, update)
    },
    add_variant: function () {
      const add = {
        variant_id: genTempKey(),
        product_id: this.productId,
        variant_title: null,
        variant_type: null,
        primary_variant: null,
        discontinued: null,
        discontinued_reason: null,
        notes: null,
        min_grams_per_unit: null,
        total_grams_per_unit: null,
        max_grams_per_unit: null,
        min_milliliters_per_unit: null,
        total_milliliters_per_unit: null,
        max_milliliters_per_unit: null,
        min_mg_per_capsule: null,
        total_mg_per_capsule: null,
        max_mg_per_capsule: null,
        total_capsules_per_unit: null,
        capsule_size: null,
        mg_empty_capsule: null
      }
      this.new_variant = cloneDeep(add)
    },
    delete_temp_variant: function (variant) {
      if (isTempKey(variant.variant_id)) {
        this.variants_buffer.splice(this.variants_buffer.indexOf(variant), 1)
        this.num_variants -= 1
        this.req.removeUpsertRecord('Product_Variant', 'variant_id', variant.variant_id)
      }
    },
    discontinue_variant: function (variant, reason) {
      if (variant.primary_variant) {
        return
      }
      variant.discontinued = true
      variant.discontinued_reason = reason
      this.update_variant(variant)
    },
    reinstate_variant: function (variant) {
      variant.discontinued = false
      variant.discontinued_reason = null
      this.update_variant(variant)
    },
    validate_fill: function (max, target, min) {
      return min !== '' && min !== null && max !== '' && max !== null && target !== '' && target !== null && min >= 0 && max >= 0 && target >= 0 && max >= target && target >= min
    },
    validate_variants_buffer: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Variant',
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

      for (const variant in this.variants_buffer) {
        if (variant.variant_type === 'powder') {
          // Powder Fill
          const pMin = variant.min_grams_per_unit
          const pMax = variant.max_grams_per_unit
          const pTarget = variant.total_grams_per_unit
          if (!this.validate_fill(pMax, pTarget, pMin)) {
            errorToast.message = 'Powder Fill values are not valid.'
            createToast(errorToast)
            valid = false
          }
        }

        if (variant.variant_type === 'capsule') {
          // Capsule Fill
          const cMin = variant.min_mg_per_capsule
          const cMax = variant.max_mg_per_capsule
          const cTarget = variant.total_mg_per_capsule
          if (!this.validate_fill(cMax, cTarget, cMin) || variant.total_capsules_per_unit === null || variant.total_capsules_per_unit === '' || variant.capsule_size === '' || variant.mg_empty_capsule === null || variant.mg_empty_capsule === '') {
            errorToast.message = 'Capsule Fill values are not valid.'
            createToast(errorToast)
            valid = false
          }
        }

        if (variant.variant_type === 'liquid') {
          // Liquid Fill
          const lMin = variant.min_milliliters_per_unit
          const lMax = variant.max_milliliters_per_unit
          const lTarget = variant.total_milliliters_per_unit
          if (!this.validate_fill(lMax, lTarget, lMin)) {
            errorToast.message = 'Liquid Fill values are not valid.'
            createToast(errorToast)
            valid = false
          }
        }
      }

      return valid
    },
    save_variants: async function () {
      // Check valid formula
      this.$emit('toggleLoaded', false)
      if (!this.validate_variants_buffer()) {
        this.$emit('toggleLoaded', true)
        return
      }

      // TODO: Conditional for new variant
      const updateProduct = {
        product_id: this.productId,
        num_product_variants: this.num_variants
      }
      this.req.upsertRecord('Product_Master', updateProduct)

      const resp = await this.req.sendRequest(window.origin)

      const createToast = this.$root.createToast
      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status === 201) {
        this.edit_variants = false
        this.$parent.edit_variants = false
        this.$parent.toggleLoaded(false)
        this.$parent.getProductData()
      } else {
        this.edit_variants = false
        this.$parent.edit_variants = false
        this.$parent.toggleLoaded(true)
      }
    },
    toggle_edit_variants: function () {
      this.edit_variants = !this.edit_variants
      this.$emit('editVariants', this.edit_variants)
    },
    cancel: function () {
      this.$emit('toggleLoaded', false)
      this.$emit('refreshParent')
      this.variants_buffer = {}
      this.req = new CustomRequest(this.$cookies.get('session'))
      this.toggle_edit_variants()
    }
  },
  created: function () {
    this.variants_buffer = cloneDeep(this.productVariants)
    this.num_variants = cloneDeep(this.numVariants)
    this.variants_buffer = this.variants_buffer.sort((a, b) => {
      if (a.primary_variant && !b.primary_variant) {
        return -1
      } else if (!a.discontinued && b.discontinued) {
        return -1
      } else if (!a.primary_variant && !b.primary_variant && !a.discontinued && !b.discontinued) {
        return 0
      } else {
        return 1
      }
    })
  }
}
</script>

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
</style>
