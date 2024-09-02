<template>
  <b-overlay :show="overlay" :opacity="1" rounded="sm">
    <b-card :id="'my_node-'+node_buffer.data.process_spec_id" style="min-width: 1200px; min-height:600px;">
      <b-card-title v-if="node_buffer.data.manufacturing_process_id">{{ node_buffer.data.process_name }}{{ variant?.variant_title ? ' - ' + variant.variant_title : '' }}
        <b-badge v-show="variant?.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
        <b-badge v-show="node_buffer.data.primary_process && !edit" class="ml-3" variant="primary">Primary</b-badge>
      </b-card-title>
      <b-card-title v-else>
        New Process
      </b-card-title>
      <b-card-sub-title class="mb-3"><b-link :href="node_buffer.data.process_sop_link" target="_blank" class="text-info">{{ node_buffer.data.process_sop }}</b-link></b-card-sub-title>
      <b-card-text class="flex-d justify-content-center">
        <div v-if="edit">
          <b-button block v-show="!node_buffer.data.primary_process" variant="outline-primary" @click="node_buffer.data.primary_process = true; updateNode()" class="mb-3">Primary</b-button>
          <b-button block v-show="node_buffer.data.primary_process" variant="primary" @click="node_buffer.data.primary_process = false; updateNode()" class="mb-3">Primary</b-button>
        </div>
        <b-container class="m-0 p-0" style="min-width:100%;">
          <b-row class="mb-3">
            <b-col v-if="!node_buffer.data.manufacturing_process_id && edit">
              <ChooseProcess
                @process="(pro) => updateProcess(pro)"
                :processes="process_options"
                :selected="getProcess()"
                :process-req="true"
                :disabled="node_buffer.data.manufacturing_process_id"
              ></ChooseProcess>
            </b-col>
          </b-row>
          <b-row class="mb-3" v-if="node_buffer.data.requires_product_variant">
            <b-col v-if="!node_buffer.data.variant_id && edit">
              <ChooseVariant
                @variant="(variant) => updateVariant(variant)"
                :variants="filteredVariantOptions"
                :selected="variant"
                :variant-req="true"
                :disabled="node_buffer.data.variant_id"
              ></ChooseVariant>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%" v-if="variant">
          <div class="d-flex justify-content-center">
            <b-button v-show="!show_variant" @click="toggleShowVariant()" class="m-1" variant="light">Show Variant Notes</b-button>
            <b-button v-show="show_variant" @click="toggleShowVariant()" class="m-1" variant="light">Hide Variant Notes</b-button>
          </div>
          <b-collapse class="mb-3" id="show_variant" v-model="show_variant">
            <b-card style="box-shadow: none;">
              <b-card-title class="d-flex justify-content-between">
                <span v-if="variant.variant_type === 'powder'">Powder Fill - {{ (variant?.total_grams_per_unit ? variant.total_grams_per_unit : 0) + 'g' }} {{ variant?.variant_title_suffix ? variant.variant_title_suffix : '' }}</span>
                <span v-if="variant.variant_type === 'liquid'">Liquid Fill - {{ (variant?.total_milliliters_per_unit ? variant.total_milliliters_per_unit : 0) + 'ml' }} {{ variant?.variant_title_suffix ? variant.variant_title_suffix : '' }}</span>
                <span v-if="variant.variant_type === 'capsule'">Capsule Fill - {{ (variant?.total_capsules_per_unit ? variant.total_capsules_per_unit : 0) + 'ct' }} {{ variant?.variant_title_suffix ? variant.variant_title_suffix : '' }}</span>
                <b-badge v-show="variant.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
                <b-badge v-show="variant.primary_variant && !edit_variants" class="ml-3" variant="primary">Primary</b-badge>
              </b-card-title>
              <b-card-text>
                <div>
                  <b-row>
                    <b-col><label for="notes"><strong>Variant Notes:</strong></label></b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <b-form-textarea
                        id="notes"
                        v-model="variant.notes"
                        disabled
                        class="form-control"
                      ></b-form-textarea>
                    </b-col>
                  </b-row>
                  <hr>
                </div>
                <div v-if="variant.variant_type === 'powder'">
                  <b-row>
                    <b-col><label :for="'manufacturing_max_grams_per_unit'+variant.variant_id"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_max_grams_per_unit'+variant.variant_id"
                          type="number"
                          v-model="variant.max_grams_per_unit"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'manufacturing_total_grams_per_unit'+variant.variant_id"><strong>Target g per Product:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_total_grams_per_unit'+variant.variant_id"
                          type="number"
                          v-model="variant.total_grams_per_unit"
                          class="form-control"
                          min="0"
                          disabled
                          aria-describedby="total_grams_per_unit-live-feedback"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'manufacturing_min_grams_per_unit'+variant.variant_id"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_min_grams_per_unit'+variant.variant_id"
                          type="number"
                          v-model="variant.min_grams_per_unit"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </div>
                <div v-if="variant.variant_type === 'liquid'">
                  <b-row>
                    <b-col><label :for="'manufacturing_max_milliliters_per_unit'+variant.variant_id"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_max_milliliters_per_unit'+variant.variant_id"
                          type="number"
                          v-model="variant.max_milliliters_per_unit"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'manufacturing_total_milliliters_per_unit'+variant.variant_id"><strong>Target ml per Product:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_total_milliliters_per_unit'+variant.variant_id"
                          type="number"
                          v-model="variant.total_milliliters_per_unit"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'manufacturing_min_milliliters_per_unit'+variant.variant_id"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_min_milliliters_per_unit'+variant.variant_id"
                          type="number"
                          v-model="variant.min_milliliters_per_unit"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </div>
                <div v-if="variant.variant_type === 'capsule'">
                  <b-row>
                    <b-col><label :for="'manufacturing_max_mg_per_capsule'+variant.variant_id"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_max_mg_per_capsule'+variant.variant_id"
                          type="number"
                          v-model="variant.max_mg_per_capsule"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'manufacturing_total_mg_per_capsule'+variant.variant_id"><strong>Target mg per Product:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_total_mg_per_capsule'+variant.variant_id"
                          type="number"
                          v-model="variant.total_mg_per_capsule"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'manufacturing_min_mg_per_capsule'+variant.variant_id"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_min_mg_per_capsule'+variant.variant_id"
                          type="number"
                          v-model="variant.min_mg_per_capsule"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <hr>
                  <b-row>
                    <b-col><label :for="'manufacturing_total_capsules_per_unit'+variant.variant_id"><strong>Capsule Count:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_total_capsules_per_unit'+variant.variant_id"
                          type="number"
                          v-model="variant.total_capsules_per_unit"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">ct</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row class="mb-2">
                    <b-col><label :for="'manufacturing_capsule_size'+variant.variant_id"><strong>Capsule Size:</strong></label></b-col>
                    <b-col>
                      <select
                        :id="'manufacturing_capsule_size'+variant.variant_id"
                        v-model="variant.capsule_size"
                        disabled
                        class="form-control"

                      >
                        <option selected value="">Select Size</option>
                        <option value="n/a">N/A</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="0">0</option>
                        <option value="00">00</option>
                    </select>
                  </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="'manufacturing_mg_empty_capsule'+variant.variant_id"><strong>Capsule Weight:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input
                          :id="'manufacturing_mg_empty_capsule'+variant.variant_id"
                          type="number"
                          v-model="variant.mg_empty_capsule"
                          required
                          min="0"
                          disabled
                          class="form-control"
                        >
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </div>
              </b-card-text>
            </b-card>
          </b-collapse>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;">
          <b-row class="mb-1">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Max Percent Loss:</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col style="max-width:100%;">
              <b-form inline>
                <b-input-group class="mr-2">
                  <div v-if="!edit">
                    <span v-show="!node_buffer.data.use_default_ave_percent_loss" class="badge badge-primary" style="font-size: 1.5em;">Custom % Loss</span>
                    <span v-show="node_buffer.data.use_default_ave_percent_loss" class="badge badge-secondary" style="font-size: 1.5em;">Default % Loss</span>
                  </div>
                  <div v-else>
                    <b-button @click="toggleDefaultPercentLoss()" v-show="!node_buffer.data.use_default_ave_percent_loss" class="badge badge-primary" style="font-size: 1.5em;">Custom % Loss</b-button>
                    <b-button @click="toggleDefaultPercentLoss()" v-show="node_buffer.data.use_default_ave_percent_loss" class="badge badge-secondary" style="font-size: 1.5em;">Default % Loss</b-button>
                  </div>
                </b-input-group>
                <b-input-group append="%" prepend="Custom:" class="mr-2">
                  <b-form-input
                    id="custom_ave_percent_loss"
                    type="number"
                    v-model="node_buffer.data.custom_ave_percent_loss"
                    min="0"
                    :disabled="!edit || node_buffer.data.use_default_ave_percent_loss"
                    :class="[node_buffer.data.custom_ave_percent_loss >= 0 || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                </b-input-group>
                <b-input-group append="%" prepend="Default:">
                  <b-form-input
                    id="ave_percent_loss"
                    type="number"
                    v-model="node_buffer.data.ave_percent_loss"
                    min="0"
                    :disabled="true"
                    class="text-center"
                    @input="updateNode()"
                  ></b-form-input>
                </b-input-group>
              </b-form>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;" v-if="node_data.data.requires_samples">
          <b-row class="mb-1">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Samples:</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col>
              <b-form inline>
                <b-input-group append="g" prepend="Lab Sample:" class="mr-2">
                  <b-form-input
                    id="lab_sample_size"
                    type="number"
                    v-model="node_buffer.data.lab_sample_size"
                    min="0"
                    :disabled="!edit"
                    :class="[node_buffer.data.lab_sample_size >= 0 || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                </b-input-group>
                <b-input-group append="g" prepend="QC Sample:" class="mr-2">
                  <b-form-input
                    id="qc_sample_size"
                    type="number"
                    v-model="node_buffer.data.qc_sample_size"
                    min="0"
                    :disabled="!edit"
                    :class="[node_buffer.data.qc_sample_size >= 0 || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                </b-input-group>
              </b-form>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;">
          <b-row class="mb-3">
            <b-col>
              <strong class="mb-1">Notes:</strong>
              <b-form-textarea
                class="mt-1"
                :disabled="!edit"
                id="textarea"
                v-model="node_buffer.data.bid_nodes"
                placeholder="Notes..."
                rows="3"
                max-rows="6"
                @input="updateNode()"
              ></b-form-textarea>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;">
          <b-row class="mb-1">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Process Setup:</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col style="max-width:100%;">
              <b-form inline>
                <b-input-group class="mr-2">
                  <div v-if="!edit">
                    <span v-show="!node_buffer.data.custom_setup_time_use_default" class="badge badge-primary" style="font-size: 1.5em;">Custom</span>
                    <span v-show="node_buffer.data.custom_setup_time_use_default" class="badge badge-secondary" style="font-size: 1.5em;">Default</span>
                  </div>
                  <div v-else>
                    <b-button @click="toggleDefaultSetup()" v-show="!node_buffer.data.custom_setup_time_use_default" class="badge badge-primary" style="font-size: 1.5em;">Custom</b-button>
                    <b-button @click="toggleDefaultSetup()" v-show="node_buffer.data.custom_setup_time_use_default" class="badge badge-secondary" style="font-size: 1.5em;">Default</b-button>
                  </div>
                </b-input-group>
                <b-input-group>
                  <b-form-input
                    id="custom_setup_time"
                    type="number"
                    v-model="node_buffer.data.custom_setup_time"
                    min="0"
                    :disabled="!edit || node_buffer.data.custom_setup_time_use_default"
                    aria-describedby="custom_setup_time-live-feedback"
                    :class="[(node_buffer.data.custom_setup_time === 0 || node_buffer.data.custom_setup_time > 0) || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                  <template #append>
                    <select :class="[node_buffer.data.custom_setup_time_units || !edit ? '' : 'is-invalid', 'text-center', 'custom-select']" v-model="node_buffer.data.custom_setup_time_units" :disabled="!edit || node_buffer.data.custom_setup_time_use_default" @change="updateNode()">
                      <option value="Seconds">Seconds</option>
                      <option value="Minutes">Minutes</option>
                      <option value="Hours">Hours</option>
                      <option value="Days">Days</option>
                    </select>
                  </template>
                </b-input-group>
                <b-input-group-text class="mx-2">with</b-input-group-text>
                <b-input-group>
                  <b-form-input
                    id="custom_setup_num_employees"
                    type="number"
                    v-model="node_buffer.data.custom_setup_num_employees"
                    min="0"
                    :disabled="!edit || node_buffer.data.custom_setup_time_use_default"
                    aria-describedby="custom_setup_num_employees-live-feedback"
                    :class="[(node_buffer.data.custom_setup_num_employees === 0 || node_buffer.data.custom_setup_num_employees > 0) || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                  <template #append>
                    <b-input-group-text>employees</b-input-group-text>
                  </template>
                </b-input-group>
              </b-form>
            </b-col>
          </b-row>
          <b-row class="mb-1">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Target Processing Rate:</strong></label></b-col>
          </b-row>
          <b-row class="mb-3 flex-nowrap">
            <b-col style="max-width:100%;">
              <b-form inline class="flex-nowrap">
                <b-input-group>
                  <b-form-input :class="[(node_buffer.data.target_process_rate === 0 || node_buffer.data.target_process_rate > 0) || !edit ? '' : 'is-invalid', 'text-center']" type="number" v-model="node_buffer.data.target_process_rate" :disabled="!edit" @input="updateNode()"></b-form-input>
                  <template #append>
                    <select :class="[node_buffer.data.target_process_rate_unit || !edit ? '' : 'is-invalid', 'text-center', 'custom-select']" :disabled="!edit" v-model="node_buffer.data.target_process_rate_unit" @change="updateNode()">
                      <option value="Products">Products</option>
                      <option value="Ingredients">Ingredients</option>
                      <option value="Barrels">Barrels</option>
                      <option value="Kilos">Kilos</option>
                      <option value="Liters">Liters</option>
                      <option value="Capsules">Capsules</option>
                      <option value="Batches">Batches</option>
                    </select>
                  </template>
                </b-input-group>
                <b-input-group-text class="mx-2">per</b-input-group-text>
                <b-input-group>
                  <b-form-input :class="[(node_buffer.data.target_process_rate_per === 0 || node_buffer.data.target_process_rate_per > 0) || !edit ? '' : 'is-invalid', 'text-center']" type="number" v-model="node_buffer.data.target_process_rate_per" :disabled="!edit" @input="updateNode()"></b-form-input>
                  <template #append>
                    <select :class="[node_buffer.data.target_process_rate_per_unit || !edit ? '' : 'is-invalid', 'text-center', 'custom-select']" v-model="node_buffer.data.target_process_rate_per_unit" :disabled="!edit" @change="updateNode()">
                      <option value="Seconds">Seconds</option>
                      <option value="Minutes">Minutes</option>
                      <option value="Hours">Hours</option>
                      <option value="Days">Days</option>
                    </select>
                  </template>
                </b-input-group>
                <b-input-group-text class="mx-2">with</b-input-group-text>
                <b-input-group>
                  <b-form-input
                    id="target_process_num_employees"
                    type="number"
                    v-model="node_buffer.data.target_process_num_employees"
                    min="0"
                    :disabled="!edit"
                    aria-describedby="target_process_num_employees-live-feedback"
                    :class="[(node_buffer.data.target_process_num_employees === 0 || node_buffer.data.target_process_num_employees > 0) || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                  <template #append>
                    <b-input-group-text>employees</b-input-group-text>
                  </template>
                </b-input-group>
              </b-form>
            </b-col>
          </b-row>
          <b-row class="mb-1">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Process Cleanup:</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col style="max-width:100%;">
              <b-form inline>
                <b-input-group class="mr-2">
                  <div v-if="!edit">
                    <span v-show="!node_buffer.data.custom_cleaning_time_use_default" class="badge badge-primary" style="font-size: 1.5em;">Custom</span>
                    <span v-show="node_buffer.data.custom_cleaning_time_use_default" class="badge badge-secondary" style="font-size: 1.5em;">Default</span>
                  </div>
                  <div v-else>
                    <b-button @click="toggleDefaultCleanup()" v-show="!node_buffer.data.custom_cleaning_time_use_default" class="badge badge-primary" style="font-size: 1.5em;">Custom</b-button>
                    <b-button @click="toggleDefaultCleanup()" v-show="node_buffer.data.custom_cleaning_time_use_default" class="badge badge-secondary" style="font-size: 1.5em;">Default</b-button>
                  </div>
                </b-input-group>
                <b-input-group>
                  <b-form-input
                    id="custom_cleaning_time"
                    type="number"
                    v-model="node_buffer.data.custom_cleaning_time"
                    min="0"
                    :disabled="!edit || node_buffer.data.custom_cleaning_time_use_default"
                    aria-describedby="custom_cleaning_time-live-feedback"
                    :class="[(node_buffer.data.custom_cleaning_time === 0 || node_buffer.data.custom_cleaning_time > 0) || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                  <template #append>
                    <select :class="[node_buffer.data.custom_cleaning_time_units || !edit ? '' : 'is-invalid', 'text-center', 'custom-select']" v-model="node_buffer.data.custom_cleaning_time_units" :disabled="!edit || node_buffer.data.custom_cleaning_time_use_default" @change="updateNode()">
                      <option value="Seconds">Seconds</option>
                      <option value="Minutes">Minutes</option>
                      <option value="Hours">Hours</option>
                      <option value="Days">Days</option>
                    </select>
                  </template>
                </b-input-group>
                <b-input-group-text class="mx-2">with</b-input-group-text>
                <b-input-group>
                  <b-form-input
                    id="custom_cleaning_num_employees"
                    type="number"
                    v-model="node_buffer.data.custom_cleaning_num_employees"
                    min="0"
                    :disabled="!edit || node_buffer.data.custom_cleaning_time_use_default"
                    aria-describedby="custom_cleaning_num_employees-live-feedback"
                    :class="[(node_buffer.data.custom_cleaning_num_employees === 0 || node_buffer.data.custom_cleaning_num_employees > 0) || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                  <template #append>
                    <b-input-group-text>employees</b-input-group-text>
                  </template>
                </b-input-group>
              </b-form>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;">
          <b-row class="mb-3">
            <b-col>
              <strong class="mb-1">Special Instructions:</strong>
              <b-form-textarea
                class="mt-1"
                :disabled="!edit"
                id="textarea"
                v-model="node_buffer.data.special_instruction"
                placeholder="Special Instruction..."
                rows="3"
                max-rows="6"
                @input="updateNode()"
              ></b-form-textarea>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;">
          <b-row v-if="!edit" class="mb-3" v-show="node_buffer.data.requires_components">
            <b-col>
              <b-table :items="node_buffer.data.process_components" :fields="component_fields" striped bordered sticky-header head-variant="light" style="max-height: 600px; min-width: 1100px;" show-empty :empty-text="'No Components Selected for this Process'">
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
            </b-col>
          </b-row>
          <b-row v-else v-show="node_buffer.data.requires_components">
            <b-col>
              <b-table :items="node_buffer.data.process_components" :fields="component_fields" striped bordered sticky-header head-variant="light" style="max-height: 600px; min-width: 1100px;" show-empty :empty-text="'No Components Selected for this Process'">
                <template #cell(components)="components">
                  <div v-for="(comp, index) in components.value" :key="comp.component_id+'-component'">
                    <b-row align-v="baseline" class="flex-nowrap">
                      <b-col style="margin: 5px; padding: 0px; margin-left: 10px; max-width: 22px;">
                        <b-badge :id="components.item.process_component_id+'-'+comp.component_id+'-component-priority'" v-bind:variant="(comp.priority === 1 ? 'primary' : 'light')" pill>{{ comp.priority }}</b-badge>
                        <b-tooltip :target="components.item.process_component_id+'-'+comp.component_id+'-component-priority'" triggers="hover">Priority Level: {{ comp.priority }}</b-tooltip>
                      </b-col>
                      <b-col style="padding: 0px; margin: 10px; max-width: 48px;">
                        <b-button @click="removeComp(components.value, components.index, index)" variant="outline-danger"><b-icon icon="trash"></b-icon></b-button>
                      </b-col>
                      <b-col style="min-width: 400px;">
                        <ChooseComponent
                          class="py-3"
                          @comp="(c) => selectComp(c, components.item.components, index)"
                          :components="filtered_component_options" :selected="comp.component_id === 0 ? null : comp"
                        ></ChooseComponent>
                      </b-col>
                    </b-row>
                    <hr v-show="index < components.value.length">
                  </div>
                  <div class="d-flex justify-content-end">
                    <b-button variant="outline-info" @click="addComp(components.item.process_component_id, components.item.components)" class="mr-3">Add Component</b-button>
                    <b-button variant="outline-danger" @click="deleteRow(components.index)">Delete Row</b-button>
                  </div>
                </template>
                <template #cell(brands)="brands">
                  <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                    <b-row align-v="baseline" class="flex-nowrap">
                      <b-col style="margin: 5px; padding: 0px; margin-left: 10px; max-width: 22px;">
                        <b-badge :id="brands.item.process_component_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill>{{ brand.priority }}</b-badge>
                        <b-tooltip :target="brands.item.process_component_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                      </b-col>
                      <b-col style="padding: 0px; margin: 10px; max-width: 48px;">
                        <b-button @click="removeBrand(brands.value, brands.index, index)" variant="outline-danger"><b-icon icon="trash"></b-icon></b-button>
                      </b-col>
                      <b-col>
                        <ChooseOrg
                          @org="(o) => selectBrand(o, brands.item.brands, index)"
                          :organizations="brand_options"
                          :selected="brand.organization_id === 0 ? null : brand"
                          :org-req="brands.item.specific_brand_required"
                        ></ChooseOrg>
                      </b-col>
                    </b-row>
                    <hr v-show="index < brands.value.length">
                  </div>
                  <div class="d-flex justify-content-end mt-2">
                    <b-button variant="outline-info" @click="addBrand(brands.item.process_component_id, brands.item.brands)">Add Brand</b-button>
                  </div>
                </template>
                <template #cell(qty_per_unit)="qty_per_unit">
                  <div class="input-group mb-2" style="font-size: 1.5em; width: 80px;">
                    <strong>
                      <input
                      :id="qty_per_unit.item.process_component_id+'-qty_per_unit'"
                      type="number" class="form-control"
                      v-model="qty_per_unit.item.qty_per_unit"
                      required
                      min="0"
                      aria-describedby="qty_per_unit-live-feedback"
                      :class="['form-control', (qty_per_unit.item.qty_per_unit > 0 ? '' : 'is-invalid')]"
                      @input="updateRow(qty_per_unit.item)"
                    >
                    </strong>
                    <div :id="qty_per_unit.item.process_component_id+'-qty_per_unit-live-feedback'" class="invalid-feedback">This required field must be greater than zero.</div>
                  </div>
                </template>
                <template #cell(specific_brand_required)="specific_brand_required">
                  <b-button @click="specific_brand_required.item.specific_brand_required = false;updateRow(specific_brand_required.item)" v-show="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                  <b-button @click="specific_brand_required.item.specific_brand_required = true;updateRow(specific_brand_required.item)" v-show="!specific_brand_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                </template>
                <template #cell(specific_component_required)="specific_component_required">
                  <b-button @click="specific_component_required.item.specific_component_required = false;updateRow(specific_component_required.item)" v-show="specific_component_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                  <b-button @click="specific_component_required.item.specific_component_required = true;updateRow(specific_component_required.item)" v-show="!specific_component_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                </template>
              </b-table>
            </b-col>
          </b-row>
          <b-row class="mb-3" v-if="edit" v-show="node_buffer.data.requires_components">
            <b-col>
              <b-button v-show="edit" block variant="outline-info" @click="addRow()">Add Row</b-button>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;" v-if="node_data.data.requires_retention">
          <b-row class="mb-1">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Retentions:</strong></label></b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col style="max-width:100%;">
              <b-form inline>
                <b-input-group append="ct" class="mr-2">
                  <b-form-input
                    id="num_retentions"
                    type="number"
                    v-model="node_buffer.data.num_retentions"
                    min="0"
                    :disabled="!edit"
                    :class="[node_buffer.data.num_retentions >= 0 || !edit ? '' : 'is-invalid', 'text-center']"
                    @input="updateNode()"
                  ></b-form-input>
                </b-input-group>
              </b-form>
            </b-col>
          </b-row>
        </b-container>
        <b-container v-if="node_buffer.data.requires_box_specs" class="m-0 p-0" style="min-width:100%;">
          <b-row class="mb-3">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Box Size:</strong></label></b-col>
            <b-col style="max-width:30%;" v-if="edit">
              <ChooseComponent
                @comp="(box) => updateBox(box)"
                :components="box_options"
                :selected="box"
                :disable-after-entry="false"
                :comp-req="false"
                no-certs
              ></ChooseComponent>
            </b-col>
            <b-col style="max-width:30%;" v-else>
              <b-link :to="'/catalogue/components/'+node_buffer.data.box_id" target="_blank"><p class="text-info">{{ box ? (box?.component_primary_name ? box.component_primary_name : (box?.component_name ? box.component_name : '')) : 'No Box Selected' }}</p></b-link>
            </b-col>
            <b-col style="max-width:20%;">
              <strong>Box Sticker Required: </strong>
            </b-col>
            <b-col class="text-center" style="max-width:30%;">
              <div v-if="!edit">
                <span v-show="node_buffer.data.box_sticker_required" class="badge badge-primary badge-pill" style="font-size: 1em;">Yes</span>
                <span v-show="!node_buffer.data.box_sticker_required" class="badge badge-secondary badge-pill" style="font-size: 1em;">No</span>
              </div>
              <div v-else>
                <b-button @click="node_buffer.data.box_sticker_required = false; updateNode()" v-show="node_buffer.data.box_sticker_required" class="badge badge-primary badge-pill" style="font-size: 1em;">Yes</b-button>
                <b-button @click="node_buffer.data.box_sticker_required = true; updateNode()" v-show="!node_buffer.data.box_sticker_required" class="badge badge-secondary badge-pill" style="font-size: 1em;">No</b-button>
              </div>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col style="max-width:20%;"><label for="box_count"><strong>Box Count:</strong></label></b-col>
            <b-col style="max-width:30%;">
              <div class="input-group mb-2">
                <input
                  id="box_count"
                  type="number"
                  v-model="node_buffer.data.qty_per_box"
                  required
                  min="0"
                  :disabled="!edit"
                  aria-describedby="box_count-live-feedback"
                  :class="['form-control', 'text-center', (node_buffer.data.qty_per_box >= 0 || !edit ? '' : 'is-invalid')]"
                  @input="updateNode()"
                >
                <div class="input-group-append">
                  <span class="input-group-text">ct</span>
                </div>
                <div id="box_count-live-feedback" class="invalid-feedback">This field must be greater than <br>or equal to zero.</div>
              </div>
            </b-col>
            <b-col style="max-width:20%;"><label for="box_weight"><strong>Average Box Weight:</strong></label></b-col>
            <b-col style="max-width:30%;">
              <div class="input-group mb-2">
                <input
                  id="box_weight"
                  type="number"
                  v-model="node_buffer.data.box_weight_in_lbs"
                  required
                  min="0"
                  :disabled="!edit"
                  aria-describedby="box_weight-live-feedback"
                  :class="['form-control', 'text-center', (node_buffer.data.box_weight_in_lbs >= 0 || !edit ? '' : 'is-invalid')]"
                  @input="updateNode()"
                >
                <div class="input-group-append">
                  <span class="input-group-text">lbs</span>
                </div>
                <div id="box_weight-live-feedback" class="invalid-feedback">This field must be greater than <br>or equal to zero.</div>
              </div>
            </b-col>
          </b-row>
          <b-row class="mb-3">
            <b-col style="max-width:20%;"><label for="boxes_per_layer"><strong>Boxes Per Layer:</strong></label></b-col>
            <b-col style="max-width:30%;">
              <div class="input-group mb-2">
                <input
                  id="boxes_per_layer"
                  type="number"
                  v-model="node_buffer.data.boxes_per_layer"
                  required
                  min="0"
                  :disabled="!edit"
                  aria-describedby="boxes_per_layer-live-feedback"
                  :class="['form-control', 'text-center', (node_buffer.data.boxes_per_layer >= 0 || !edit ? '' : 'is-invalid')]"
                  @input="updateNode()"
                >
                <div class="input-group-append">
                  <span class="input-group-text">ct</span>
                </div>
                <div id="boxes_per_layer-live-feedback" class="invalid-feedback">This field must be greater than <br>or equal to zero.</div>
              </div>
            </b-col>
            <b-col style="max-width:20%;"><label for="max_pallet_layers"><strong>Max Pallet Layers:</strong></label></b-col>
            <b-col style="max-width:30%;">
              <div class="input-group mb-2">
                <input
                  id="max_pallet_layers"
                  type="number"
                  v-model="node_buffer.data.max_pallet_layers"
                  required
                  min="0"
                  :disabled="!edit"
                  aria-describedby="max_pallet_layers-live-feedback"
                  :class="['form-control', 'text-center', (node_buffer.data.max_pallet_layers >= 0 || !edit ? '' : 'is-invalid')]"
                  @input="updateNode()"
                >
                <div class="input-group-append">
                  <span class="input-group-text">ct</span>
                </div>
                <div id="max_pallet_layers-live-feedback" class="invalid-feedback">This field must be greater than <br>or equal to zero.</div>
              </div>
            </b-col>
          </b-row>
        </b-container>
        <b-container class="m-0 p-0" style="min-width:100%;">
          <b-row class="mb-3">
            <b-col>
              <b-table :items="sortEquipment(node_buffer.data.equipment)" :fields="equipment_fields" striped bordered sticky-header head-variant="light" style="max-height: 600px; min-width: 1100px;" show-empty :empty-text="'No Equipment Needed for this Process'">
                <template #cell(equipment_name)="equipment_name">
                  <b-button v-on:click.stop class="mr-2" variant="light" :to="'/manufacturing/equipment/'+equipment_name.item.equipment_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
                  <b class="text-info">{{ equipment_name.value }}</b>
                </template>
                <template #cell(status)="status">
                  <h4 v-if="status.value === 'Working_Order'"><b-badge variant="success">{{ status.value.replace('_', ' ') }}</b-badge></h4>
                  <h4 v-if="status.value === 'Broken'"><b-badge variant="danger">{{ status.value.replace('_', ' ') }}</b-badge></h4>
                  <h4 v-if="status.value === 'Removed'"><b-badge variant="light">{{ status.value.replace('_', ' ') }}</b-badge></h4>
                </template>
              </b-table>
            </b-col>
          </b-row>
        </b-container>
      </b-card-text>
      <Handle v-if="node_buffer.data.top_handle" id="a" type="target" class="custom_vue-flow__handle" :position="top" />
      <Handle v-if="node_buffer.data.bottom_handle" id="b" type="source" class="custom_vue-flow__handle" :position="bottom" />
      <NodeToolbar :is-visible="node_data.toolbarVisible" :position="bottom" :align="'end'">
        <b-button v-show="edit" variant="outline-danger" @click="deleteNode()">Delete Process</b-button>
      </NodeToolbar>
    </b-card>
    <template #overlay>
      <div class="text-center" style="width: 100%;">
        <strong style="font-size: 6em;">{{ node_buffer.data.process_name }}{{ variant?.variant_title ? ' - ' + variant.variant_title : '' }}</strong>
        <b-badge style="font-size: 6em;" v-show="variant?.discontinued" class="ml-3" variant="danger">Discontinued</b-badge>
        <b-badge style="font-size: 6em;" v-show="node_buffer.data.primary_process" class="ml-3" variant="primary">Primary</b-badge>
      </div>
    </template>
  </b-overlay>
</template>

<style scoped>
.btn {
  white-space: nowrap
}
.custom_vue-flow__handle {
  width: 32px;
  height: 32px;
}
.card {
  box-shadow: 0 10px 10px rgba(0,0,0,.2);
}
.custom-row {
  border-bottom-width: thick !important;
  border-top-width: thick !important;
}
</style>

<script>
import { Handle, Position } from '@vue-flow/core'
import { NodeToolbar } from '@vue-flow/node-toolbar'
import CertBadge from '../../../components/CertBadge.vue'
import { genTempKey } from '../../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import ChooseComponent from '../../../components/ChooseComponent.vue'
import ChooseOrg from '../../../components/ChooseOrg.vue'
import ChooseProcess from '../../../components/ChooseProcess.vue'
import ChooseVariant from '../../../components/ChooseVariant.vue'

export default {
  data: function () {
    return {
      right: Position.Right,
      left: Position.Left,
      top: Position.Top,
      bottom: Position.Bottom,
      node_buffer: null,
      component_fields: [
        { label: 'Component', key: 'components', tdClass: 'custom-row' },
        { label: 'Brands', key: 'brands', tdClass: 'custom-row' },
        { label: 'Qty', key: 'qty_per_unit', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Brand Specific', key: 'specific_brand_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Component Specific', key: 'specific_component_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' }
      ],
      equipment_fields: [
        { label: 'Equipment', key: 'equipment_name' },
        { label: 'Serial No.', key: 'equipment_sn' },
        { label: 'Status', key: 'status' }
      ],
      variant: null,
      show_variant: false
    }
  },
  props: {
    node_data: {
      required: true,
      type: Object
    },
    edit: {
      required: true,
      type: Boolean
    },
    id: {
      required: true
    },
    component_options: {
      required: true,
      type: Array
    },
    brand_options: {
      required: true,
      type: Array
    },
    process_options: {
      required: true,
      type: Array
    },
    variant_options: {
      required: true,
      type: Array
    },
    overlay: {
      required: true,
      type: Boolean
    }
  },
  components: {
    Handle,
    NodeToolbar,
    CertBadge,
    ChooseComponent,
    ChooseOrg,
    ChooseProcess,
    ChooseVariant
  },
  methods: {
    toggleShowVariant: function () {
      this.show_variant = !this.show_variant
      // wait 1 second before resizing node
      setTimeout(() => {
        this.$emit('resizeNode', this.node_buffer.data)
      }, 1000)
    },
    toggleDefaultPercentLoss: function () {
      this.node_buffer.data.use_default_ave_percent_loss = !this.node_buffer.data.use_default_ave_percent_loss
      if (this.node_buffer.data.use_default_ave_percent_loss) {
        this.node_buffer.data.custom_ave_percent_loss = this.node_buffer.data.ave_percent_loss
      }
      this.updateNode()
    },
    toggleDefaultSetup: function () {
      this.node_buffer.data.custom_setup_time_use_default = !this.node_buffer.data.custom_setup_time_use_default
      if (this.node_buffer.data.custom_setup_time_use_default) {
        this.node_buffer.data.custom_setup_time = this.node_buffer.data.setup_time
        this.node_buffer.data.custom_setup_time_units = this.node_buffer.data.setup_time_units
        this.node_buffer.data.custom_setup_num_employees = this.node_buffer.data.setup_num_employees
      }
      this.updateNode()
    },
    toggleDefaultCleanup: function () {
      this.node_buffer.data.custom_cleaning_time_use_default = !this.node_buffer.data.custom_cleaning_time_use_default
      if (this.node_buffer.data.custom_cleaning_time_use_default) {
        this.node_buffer.data.custom_cleaning_time = this.node_buffer.data.cleaning_time
        this.node_buffer.data.custom_cleaning_time_units = this.node_buffer.data.cleaning_time_units
        this.node_buffer.data.custom_cleaning_num_employees = this.node_buffer.data.cleaning_num_employees
      }
      this.updateNode()
    },
    updateBox: function (box) {
      this.node_buffer.data.box_id = box.component_id
      this.updateNode()
    },
    getVariant: function () {
      if (this.variant !== null) {
        return
      }
      if (!this.node_buffer.data.variant_id) {
        this.variant = null
        return
      }
      this.variant = this.variant_options.find((v) => v.variant_id === this.node_buffer.data.variant_id)
    },
    updateVariant: function (variant) {
      this.variant = variant
      this.node_buffer.data.variant_id = variant.variant_id
      this.updateNode()
    },
    removeBrand: function (brands, rowIndex, brandIndex) {
      this.$emit('deleteNodeRowBrand', cloneDeep(this.node_buffer.data), rowIndex, brandIndex)
      for (let i = brandIndex; i < brands.length; i++) {
        brands[i].priority = i + 1
      }
    },
    selectBrand: function (org, brands, index) {
      if (org !== null) {
        const brand = {
          _id: brands[index]._id,
          brand_id: org.organization_id,
          priority: brands[index].priority,
          process_component_id: brands[index].process_component_id,
          ...org,
          timestamp_fetched: org.timestamp_fetched
        }
        brands[index] = brand
        this.updateRow()
      }
    },
    addBrand: function (processComponentId, brands) {
      const newBrand = {
        _id: genTempKey(),
        process_component_id: processComponentId,
        brand_id: 0,
        priority: brands.length + 1,
        timestamp_fetched: new Date().toISOString()
      }
      brands.push(newBrand)
      this.updateRow()
    },
    removeComp: function (components, rowIndex, compIndex) {
      this.$emit('deleteNodeRowComponent', cloneDeep(this.node_buffer.data), rowIndex, compIndex)
      for (let i = compIndex; i < components.length; i++) {
        components[i].priority = i + 1
      }
    },
    selectComp: function (comp, components, index) {
      if (comp !== null) {
        const component = {
          _id: components[index]._id,
          component_id: comp.component_id,
          priority: components[index].priority,
          process_component_id: components[index].process_component_id,
          ...comp,
          timestamp_fetched: comp.timestamp_fetched
        }
        components[index] = component
        this.updateRow()
      }
    },
    addComp: function (processComponentId, components) {
      const newComponent = {
        _id: genTempKey(),
        process_component_id: processComponentId,
        component_id: 0,
        priority: components.length + 1,
        timestamp_fetched: new Date().toISOString()
      }
      components.push(newComponent)
      this.updateRow()
    },
    deleteRow: function (index) {
      this.$emit('deleteNodeRow', cloneDeep(this.node_buffer.data), index)
    },
    updateRow: function () {
      this.updateNode()
    },
    addRow: function () {
      const processComponentId = genTempKey()
      const newRow = {
        process_spec_id: this.id,
        process_component_id: processComponentId,
        qty_per_unit: 0,
        specific_brand_required: false,
        specific_component_required: false,
        components: [
          {
            _id: genTempKey(),
            process_component_id: processComponentId,
            component_id: 0,
            priority: 1
          }
        ],
        brands: [],
        timestamp_fetched: new Date().toISOString()
      }
      this.node_buffer.data.process_components.push(newRow)
      this.updateNode()
    },
    sortEquipment: function (equipment) {
      return equipment.sort((a, b) => {
        if (a.status === b.status) {
          return 0
        } else if ((a.status === 'Working_Order' && b.status !== 'Working_Order') || b.status === 'Removed') {
          return -1
        } else {
          return 1
        }
      })
    },
    updateProcess: function (newProcess) {
      this.node_buffer.data = {
        ...this.node_buffer.data,
        ...cloneDeep(newProcess)
      }
      this.node_buffer.data.manufacturing_process_id = newProcess.process_id
      if (this.node_buffer.data.use_default_ave_percent_loss) {
        this.node_buffer.data.custom_ave_percent_loss = this.node_buffer.data.ave_percent_loss
      }
      if (this.node_buffer.data.custom_setup_time_use_default) {
        this.node_buffer.data.custom_setup_time = this.node_buffer.data.setup_time
        this.node_buffer.data.custom_setup_time_units = this.node_buffer.data.setup_time_units
        this.node_buffer.data.custom_setup_num_employees = this.node_buffer.data.setup_num_employees
      }
      if (this.node_buffer.data.custom_cleaning_time_use_default) {
        this.node_buffer.data.custom_cleaning_time = this.node_buffer.data.cleaning_time
        this.node_buffer.data.custom_cleaning_time_units = this.node_buffer.data.cleaning_time_units
        this.node_buffer.data.custom_cleaning_num_employees = this.node_buffer.data.cleaning_num_employees
      }
      this.updateNode()
    },
    getProcess: function () {
      const processData = {
        process_id: this.node_buffer.data.manufacturing_process_id,
        process_name: this.node_buffer.data.process_name,
        process_sop: this.node_buffer.data.process_sop
      }
      return processData
    },
    updateNode: function () {
      this.$nextTick(() => {
        this.$emit('updateNodeData', this.node_buffer.data)
      })
    },
    deleteNode: function () {
      this.$emit('deleteNode', this.node_buffer.data)
    }
  },
  computed: {
    box_options: function () {
      if (!this.component_options) {
        return []
      }
      return this.component_options.filter((c) => c.component_type === 'box')
    },
    box: function () {
      if (!this.node_buffer.data.box_id) {
        return null
      }
      return this.component_options.find((c) => c.component_id === this.node_buffer.data.box_id)
    },
    filteredVariantOptions: function () {
      if (this.node_buffer.data.product_variant_type === null) {
        return this.variant_options
      }
      return this.variant_options.filter(variant => variant.variant_type === this.node_buffer.data.product_variant_type)
    },
    filtered_component_options: function () {
      if (!this.component_options) {
        return []
      }
      if (!this.node_buffer.component_filters) {
        return this.component_options
      }
      const filter = this.node_buffer.data.component_filters
      return this.component_options.filter((c) => filter.indexOf(c.component_type) > -1)
    }
  },
  created: function () {
    this.node_buffer = cloneDeep(this.node_data)
    const filter = this.node_buffer.data.component_filters
    console.log('component_filters', filter)
    this.getVariant()
  }
}
</script>
