<template>
  <div class="d-flex justify-content-center my_component">
    <b-card class="my-2" v-show="!loaded">
      <b-card-body>
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </b-card-body>
    </b-card>

    <div v-if="loaded" style="width: 100%;">
      <div
        v-b-visible="handleVisible"
        class="position-fixed d-block d-lg-none"
        style="z-index: 20000; height: 1px;"
      ></div>
      <div>
        <b-card class="my-2">
          <b-card-title>
            <b-container fluid class="p-0 m-0">
              <b-row>
                <b-col>
                  <h2>
                    <router-link class="text-info" v-show="!isMd" :to="'/organizations/'+order.client[0].organization_id" target="_blank">{{ order.client[0].organization_name }}</router-link>
                    Order: {{ order.client_po_num }}
                  </h2>
                </b-col>
                <b-col class="d-flex justify-content-end">
                  <div>
                    <!-- <b-button @click="toggleAssignLotNumbers()" v-if="!order.lot_num_assigned" v-show="!assign_lot_numbers_mode" class="mr-2 mb-2" variant="outline-primary" :block="isMd">Assign Lot Numbers</b-button> -->
                    <b-badge v-if="!order.lot_num_assigned" variant="warning" class="p-2" :block="isMd">
                      <b-icon icon="exclamation-triangle-fill"></b-icon> Batch & Lot Number Assignment Incomplete
                    </b-badge>
                  </div>
                </b-col>
              </b-row>
            </b-container>
          </b-card-title>
          <b-card-sub-title>
            {{ order.prefix }} {{ order.year ? order.year.toString().padStart(2, '0') : '' }}-{{ order.sec_number ? order.sec_number.toString().padStart(3, '0') : '' }} {{ order.suffix }}
          </b-card-sub-title>
          <b-card-body>
            <b-container fluid class="m-0 p-0" v-show="!assign_lot_numbers_mode">
              <b-row align-v="center">
                <b-col md="3" class="mb-2">
                  <b>Date Ordered: </b>
                  <div>
                    <b-form-datepicker
                      id="order_date"
                      v-model="order.order_date"
                    ></b-form-datepicker>
                  </div>
                </b-col>
                <b-col md="3" class="mb-2">
                  <b>Target Due Date: </b>
                  <div>
                    <b-form-datepicker
                      id="target_completion_date"
                      v-model="order.target_completion_date"
                    ></b-form-datepicker>
                  </div>
                </b-col>
                <b-col md="3" class="mb-2">
                  <b>Billed Date: </b>
                  <div>
                    <b-form-datepicker
                      id="billed_date"
                      v-model="order.billed_date"
                    ></b-form-datepicker>
                  </div>
                </b-col>
                <b-col md="3" class="mb-2">
                  <b>Closed Date: </b>
                  <div>
                    <b-form-datepicker
                      id="closed_date"
                      v-model="order.closed_date"
                    ></b-form-datepicker>
                  </div>
                </b-col>
              </b-row>
            </b-container>
            <div class="d-print-none" v-show="!assign_lot_numbers_mode">
              <h4 id="OrderDocuments">Order Documents<b-button v-if="!edit_documents" v-b-tooltip.hover title="Edit Documents" @click="edit_documents = true" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h4>
              <b-card-group class="ml-3">
                <div v-for="(document, index) in sale_order_files_buffer" :key="index">
                  <b-card class="m-2 custom_card" style="min-width: 22rem; max-width: 22rem;" no-body>
                    <b-card-body>
                      <b-card-title class="my-1" v-show="document.document_type">
                        {{ document.document_type === 'purchase_order' ? 'Purchase Order' : null }}
                        {{ document.document_type === 'email' ? 'Email' : null }}
                        {{ document.document_type === 'invoice' ? 'Invoice' : null }}
                        {{ document.document_type === 'other' ? 'Other' : null }}
                      </b-card-title>
                      <v-select v-show="!document.document_type" v-model="document.document_type" required label="text" :reduce="doc => doc.value" placeholder="Select Document Type"
                        :options="[
                          { value: 'purchase_order', text: 'Purchase Order' },
                          { value: 'email', text: 'Email' },
                          { value: 'invoice', text: 'Invoice' },
                          { value: 'other', text: 'Other' }
                        ]">
                      </v-select>
                      <strong>Document Name: </strong><br><b-form-input :disabled="!edit_documents" v-model="document.name" type="text" class="my-1"></b-form-input>
                      <strong>Description: </strong><br><b-form-textarea :disabled="!edit_documents" v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                      <b-form-file v-if="!document.file_hash && edit_documents" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                      <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                    </b-card-body>
                    <b-card-footer>
                      <b-button block v-show="edit_documents" :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(order.doc.sale_order_files, document)">Delete Document</b-button>
                      <div v-show="!edit_documents">Upload Date: {{ new Date(document.date_uploaded).toLocaleDateString() }}</div>
                    </b-card-footer>
                  </b-card>
                </div>
                <b-card class="m-2 custom_card" v-if="edit_documents" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument(order.doc.sale_order_files)">
                  <b-card-title>Add Document</b-card-title>
                </b-card>
                <b-card class="custom_card" v-if="edit_documents && orders?.doc?.sale_order_files?.length === 0">
                  <b-card-title>No Documents Yet</b-card-title>
                </b-card>
              </b-card-group>
              <div class="d-flex my-3">
                <div v-show="edit_documents">
                  <b-button type="submit" variant="outline-success" class="m-2" v-on:click="saveDocs()">Save</b-button>
                  <b-button variant="outline-danger" class="m-2" v-on:click="toggleEditDocs()">Cancel</b-button>
                </div>
              </div>
            </div>
            <div class="d-flex justify-content-between mb-2">
              <h4>Order Details</h4>
              <b-button @click="toggleAssignLotNumbers()" v-if="!order.lot_num_assigned" v-show="!assign_lot_numbers_mode" class="ml-2" variant="outline-primary">Assign Batch & Lot Numbers</b-button>
            </div>
            <OrderDetailsTable :order-details="order.sale_order_detail"></OrderDetailsTable>
            <div style="position:relative; max-height:60vh; overflow-y:scroll;border: 1px solid lightgray;" v-show="assign_lot_numbers_mode">
              <b-card-group class="d-flex flex-column p-2">
                <div v-for="batch, index in batches" :key="index">
                  <b-card class="custom_card mb-2" style="width: 100%;" no-body>
                    <b-card-title class="m-3 d-flex justify-content-between">
                      <div class="m-2 d-flex flex-row align-items-center">
                        <h3 class="m-0">Batch #{{ index + 1 }}:
                          <router-link v-if="batch.product_with_formula_selected" class="mr-2 mt-2 text-info" :to="'/catalogue/products/'+batch.product_id" target="_blank">
                            {{ batch.title }}
                          </router-link>
                        </h3>
                        <h6 v-if="batch.product_with_formula_selected"><CertBadge :data="batch.product[0]" size="3em"></CertBadge></h6>
                      </div>
                      <div>
                        <b-button :disabled="!batch.product_with_formula_selected" variant="outline-info" class="text-nowrap mr-2" @click="copyBatch(index)">Copy Batch</b-button>
                        <b-button variant="outline-danger" class="text-nowrap" @click="deleteBatch(index)">Remove Batch</b-button>
                      </div>
                    </b-card-title>
                    <b-card-body>
                      <b-container v-if="!batch.product_with_formula_selected" fluid>
                        <b-row class="mb-2">
                          <b-col md="3">
                            <span><strong>Select Product Formula: </strong></span>
                          </b-col>
                          <b-col class="d-flex flex-row flex-nowrap">
                            <ChooseProductWithFormula :products-with-formulas="product_with_formula_menu" :selected="batch" @product-with-formula="(pwf) => selectProductWithFormula(index, pwf)" :disabled="false" :product-req="true"></ChooseProductWithFormula>
                          </b-col>
                        </b-row>
                      </b-container>
                      <b-container v-if="batch.product_with_formula_selected" fluid class="mb-3">
                        <b-row>
                          <b-col md="2" class="mb-2" align-v="center" v-b-tooltip.hover title="Allocate multiple productions to one batch. This saves time and labor. The default is one production per one batch.">
                            <b>Multiple Variants: </b>
                            <div class="d-flex justify-content-center mr-2 w-100">
                              <b-button @click="batch.multiple_variants = false" v-show="batch.multiple_variants" class="badge badge-info w-100" style="font-size: 1.4em;">Yes</b-button>
                              <b-button @click="batch.multiple_variants = true" v-show="!batch.multiple_variants" class="badge badge-light w-100" style="font-size: 1.4em;">No</b-button>
                            </div>
                          </b-col>
                          <b-col md="2" class="mb-2" v-b-tooltip.hover title="Is this a 'Powder' or 'Liquid' batch?">
                            <b>Batch Type:</b>
                            <v-select v-model="batch.batch_type" required label="text" :reduce="doc => doc.value" placeholder="Batch Type" :clearable="false"
                            :options="[
                              { value: 'Powder', text: 'Powder' },
                              { value: 'Liquid', text: 'Liquid' }
                            ]">
                            </v-select>
                          </b-col>
                          <b-col md="2" class="mb-2" v-b-tooltip.hover title="The total batch size.  All production allocations must sum to this total.">
                            <b>Batch Size: </b>
                            <div class="input-group">
                              <b-form-input v-model="batch.batch_size" type="number" @input="syncBatchWithAllocated(index, 'batch');updateBatch(index)"
                                aria-describedby="batch_size-live-feedback"
                                :class="[(!batch.batch_requires_blending || (batch.batch_size > 0 && batch.batch_size !== null && batch.batch_size !== '') ? '' : 'is-invalid')]"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span v-if="batch.batch_type === 'Powder'" class="input-group-text">Kg</span>
                                <span v-else-if="batch.batch_type === 'Liquid'" class="input-group-text">L</span>
                                <span v-else class="input-group-text">?</span>
                              </div>
                              <div id="batch_size-live-feedback" class="invalid-feedback">This required field must be greater than 0.</div>
                            </div>
                          </b-col>
                          <b-col md="2" class="mb-2" align-v="center" v-b-tooltip.hover title="If there are multiple ingredients in the selected formula, blending should be required.">
                            <b>Blending Required: </b>
                            <div class="d-flex justify-content-center mr-2 w-100">
                              <b-button @click="batch.batch_requires_blending = false" v-show="batch.batch_requires_blending" class="badge badge-info w-100" style="font-size: 1.4em;">Yes</b-button>
                              <b-button @click="batch.batch_requires_blending = true" v-show="!batch.batch_requires_blending" class="badge badge-light w-100" style="font-size: 1.4em;">No</b-button>
                            </div>
                          </b-col>
                          <b-col md="2" class="mb-2" v-b-tooltip.hover title="Use this to ensure the total batch can fit in the blender.">
                            <b>Max Blender Capacity: </b>
                            <div class="input-group">
                              <b-form-input v-model="batch.max_blender_capacity" type="number"
                                aria-describedby="batch_size-live-feedback"
                                :class="[(!batch.batch_requires_blending || (batch.max_blender_capacity > 0 && batch.max_blender_capacity !== null && batch.max_blender_capacity !== '') ? '' : 'is-invalid')]"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span v-if="batch.batch_type === 'Powder'" class="input-group-text">Kg</span>
                                <span v-else-if="batch.batch_type === 'Liquid'" class="input-group-text">L</span>
                                <span v-else class="input-group-text">?</span>
                              </div>
                              <div id="batch_size-live-feedback" class="invalid-feedback">This required field must be greater than 0.</div>
                            </div>
                          </b-col>
                        </b-row>
                        <!-- <b-row class="mb-2">
                          <b-col md="2">
                            <span><strong>Avaliable Productions: </strong></span>
                          </b-col>
                          <b-col>
                            <pre>{{ JSON.stringify(batch.productions_allowed, null, 4) }}</pre>
                          </b-col>
                        </b-row> -->
                      </b-container>
                      <b-container v-if="batch.product_with_formula_selected" fluid class="mt-3 border rounded p-3">
                        <b-row class="my-1">
                          <b-col col md="auto">
                            <strong>Prod #</strong>
                          </b-col>
                          <b-col md="3">
                            <strong>Product</strong>
                          </b-col>
                          <b-col>
                            <strong>Bulk Allocated</strong>
                          </b-col>
                          <b-col>
                            <strong>Percent Loss</strong>
                          </b-col>
                          <b-col>
                            <strong>Target Unit Yield</strong>
                          </b-col>
                          <b-col>
                            <strong>Min Unit Yield</strong>
                          </b-col>
                          <b-col>
                            <strong>Max Unit Yield</strong>
                          </b-col>
                        </b-row>
                        <div v-for="production, pindex in batch.productions" :key="pindex">
                          <hr>
                          <b-row class="my-1">
                            <b-col col md="auto">
                              <h4><b-badge variant="info">{{ pindex + 1 }}</b-badge></h4>
                            </b-col>
                            <b-col md="3">
                              <div v-if="!production.variant">
                                <ChooseVariant :variants="getVariants(batch)" :selected="production.variant" @variant="(v) => batch.productions[pindex] = updateProduction(batch.productions[pindex], v, index, pindex)" :disabled-prop="false" :variant-req="true"></ChooseVariant>
                              </div>
                              <div v-else class="input-group">
                                <b-form-input disabled :value="batch.title + ' ' + production.variant.variant_title">
                                {{ batch.title }} {{ production.variant.variant_title }}
                                </b-form-input>
                                <div class="input-group-append">
                                  <b-button @click="deleteProductionRun(index, pindex)" variant="outline-danger">
                                    <b-icon icon="trash"></b-icon>
                                  </b-button>
                                </div>
                              </div>
                            </b-col>
                            <b-col>
                              <div class="input-group">
                                <b-form-input v-model="production.allocated_batch_size" @input="calculateYield(index, production);syncBatchWithAllocated(index, 'production')" type="number"
                                  aria-describedby="allocated_batch_size-live-feedback"
                                  :disabled="!production.variant_id"
                                  :class="[(validAllocation(production, batch) ? '' : 'is-invalid')]"
                                ></b-form-input>
                                <div class="input-group-append">
                                  <span v-if="batch.batch_type === 'Powder'" class="input-group-text">Kg</span>
                                  <span v-else-if="batch.batch_type === 'Liquid'" class="input-group-text">L</span>
                                  <span v-else class="input-group-text">?</span>
                                </div>
                                <div id="allocated_batch_size-live-feedback" class="invalid-feedback">This required field must be between 0 and {{ batch.max_blender_capacity }}.</div>
                              </div>
                            </b-col>
                            <b-col>
                              <div class="input-group">
                                <b-form-input v-model="production.percent_loss" @input="calculateYield(index, production)" type="number"
                                  aria-describedby="percent_loss-live-feedback"
                                  :disabled="!production.variant_id"
                                  :class="[(production.percent_loss > 0 && production.percent_loss <= 100 ? '' : 'is-invalid')]"
                                ></b-form-input>
                                <div class="input-group-append">
                                  <span class="input-group-text">%</span>
                                </div>
                                <div id="percent_loss-live-feedback" class="invalid-feedback">This required field must be greater than 0 and between 0 and 100.</div>
                              </div>
                            </b-col>
                            <b-col>
                              <div class="input-group">
                                <div class="input-group-prepend">
                                  <span class="input-group-text">Tgt</span>
                                </div>
                                <b-form-input v-model="production.target_unit_yield" type="number"
                                  aria-describedby="target_unit_yield-live-feedback"
                                  :class="[(production.target_unit_yield > production.min_unit_yield && production.target_unit_yield < production.max_unit_yield ? '' : 'is-invalid')]"
                                  disabled
                                ></b-form-input>
                                <div class="input-group-append">
                                  <span class="input-group-text">ct</span>
                                </div>
                              </div>
                            </b-col>
                            <b-col>
                              <div class="input-group">
                                <div class="input-group-prepend">
                                  <span class="input-group-text">Min</span>
                                </div>
                                <b-form-input v-model="production.min_unit_yield" type="number"
                                  aria-describedby="min_unit_yield-live-feedback"
                                  disabled
                                ></b-form-input>
                                <div class="input-group-append">
                                  <span class="input-group-text">ct</span>
                                </div>
                              </div>
                            </b-col>
                            <b-col>
                              <div class="input-group">
                                <div class="input-group-prepend">
                                  <span class="input-group-text">Max</span>
                                </div>
                                <b-form-input v-model="production.max_unit_yield" type="number"
                                  aria-describedby="max_unit_yield-live-feedback"
                                  disabled
                                ></b-form-input>
                                <div class="input-group-append">
                                  <span class="input-group-text">ct</span>
                                </div>
                              </div>
                            </b-col>
                          </b-row>
                        </div>
                        <b-row class="m-3" v-if="batch.multiple_variants || batch.productions.length < 1">
                          <b-button block variant="outline-info" @click="addProductionRun(index)" v-if="batch.product_with_formula_selected">Create Production Run (Lot#)</b-button>
                        </b-row>
                      </b-container>
                      <b-container class="m-0 mt-3" v-if="batch.product_with_formula_selected" fluid>
                        <b-row>
                          <b-col md="3" class="mb-2">
                            <div class="input-group">
                              <div class="input-group-prepend">
                                <span class="input-group-text">Batch Size:</span>
                              </div>
                              <b-form-input v-model="batch.batch_size" type="number"
                                disabled
                                aria-describedby="batch_size-live-feedback"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span v-if="batch.batch_type === 'Powder'" class="input-group-text">Kg</span>
                                <span v-else-if="batch.batch_type === 'Liquid'" class="input-group-text">L</span>
                                <span v-else class="input-group-text">?</span>
                              </div>
                            </div>
                          </b-col>
                          <b-col md="3" class="mb-2">
                            <div class="input-group">
                              <div class="input-group-prepend">
                                <span class="input-group-text">Batch Allocated:</span>
                              </div>
                              <b-form-input v-model="batch.batch_allocated" type="number"
                                aria-describedby="batch_allocated-live-feedback"
                                disabled
                                :class="[(batch.batch_allocated > 0? 'is-valid' : 'is-invalid')]"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span v-if="batch.batch_type === 'Powder'" class="input-group-text">Kg</span>
                                <span v-else-if="batch.batch_type === 'Liquid'" class="input-group-text">L</span>
                                <span v-else class="input-group-text">?</span>
                              </div>
                              <div id="batch_allocated-live-feedback" class="invalid-feedback">This required field must be greateer than 0.</div>
                            </div>
                          </b-col>
                          <b-col md="3" class="mb-2">
                            <div class="input-group">
                              <div class="input-group-prepend">
                                <span class="input-group-text">Batch Remaining:</span>
                              </div>
                              <b-form-input v-model="batch.batch_remaining" type="number"
                                aria-describedby="batch_remaining-live-feedback"
                                disabled
                                :class="[(batch.batch_remaining === 0? 'is-valid' : 'is-invalid')]"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span v-if="batch.batch_type === 'Powder'" class="input-group-text">Kg</span>
                                <span v-else-if="batch.batch_type === 'Liquid'" class="input-group-text">L</span>
                                <span v-else class="input-group-text">?</span>
                              </div>
                              <div id="batch_remaining-live-feedback" class="invalid-feedback">This required field must be equal to 0.</div>
                            </div>
                          </b-col>
                          <b-col md="3" class="mb-2">
                            <div class="input-group">
                              <div class="input-group-prepend">
                                <span class="input-group-text">Batch Size</span>
                              </div>
                              <b-form-input :value="batch.batch_requires_blending ? '≤' : '≠'" type="text" style="width: 4rem;"
                                aria-describedby="batch_le_blend-live-feedback"
                                disabled
                                :class="[(!batch.batch_requires_blending || (batch.batch_size <= batch.max_blender_capacity)? 'is-valid' : 'is-invalid')]"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span class="input-group-text">Blender Capacity</span>
                              </div>
                              <div id="batch_le_blend-live-feedback" class="invalid-feedback">Batch size must be less than or equal to the blender capacity.</div>
                            </div>
                          </b-col>
                        </b-row>
                      </b-container>
                    </b-card-body>
                  </b-card>
                </div>
                <b-card id="add-product" class="custom_card mb-2" style="width: 100%;cursor: pointer;" no-body @click="addBatch()">
                  <b-card-body class="d-flex justify-content-center align-items-center">
                    <b-icon icon="plus-lg" size="2rem"></b-icon>
                    <b class="ml-2">Create a Batch (Batch#)</b>
                  </b-card-body>
                </b-card>
                <b-tooltip target="add-product" triggers="hover">Create a batch, allocate the batch to products.</b-tooltip>
              </b-card-group>
              <!-- <pre>{{ JSON.stringify(order, null, 4) }}</pre> -->
            </div>
            <div class="mt-3" v-if="assign_lot_numbers_mode">
              <b-button :disabled="!order.lot_num_assigned" class="mr-2" variant="outline-success" @click="saveBatchAndLotNumbers()">Save</b-button>
              <b-button variant="outline-danger" to="/orders/so">Cancel</b-button>
            </div>
          </b-card-body>
        </b-card>
      </div>
    </div>
  </div>
</template>

<script>
import vSelect from 'vue-select'
import { CustomRequest, genTempKey } from '../../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import OrderDetailsTable from './OrderDetailsTable.vue'
import ChooseProductWithFormula from '@/components/ChooseProductWithFormula.vue'
import ChooseVariant from '@/components/ChooseVariant.vue'
import CertBadge from '@/components/CertBadge.vue'

export default {
  name: 'SaleOrderDetail',
  components: {
    vSelect,
    OrderDetailsTable,
    ChooseProductWithFormula,
    CertBadge,
    ChooseVariant
  },
  data: function () {
    return {
      loaded: false,
      id: this.$route.params.id,
      edit_documents: false,
      le: '≤',
      batches: [],
      order: {},
      fields: [
        { key: 'product_name', label: 'Product', sortable: true },
        { key: 'certs', label: 'Certs' }
      ],
      req: new CustomRequest(this.$cookies.get('session')),
      isMd: false,
      assign_lot_numbers_mode: false
    }
  },
  computed: {
    product_with_formula_menu: function () {
      const productWithFormula = {}
      this.order.sale_order_detail.forEach((detail) => {
        const key = `product_${detail.product_id}-formula_${detail.formula_id}`
        productWithFormula[key] = {
          id: key,
          formula_id: detail.formula_id,
          product_id: detail.product_id,
          formula: detail.formula,
          product: detail.product,
          title: `${detail.product[0].product_name} V${detail.formula[0].formulation_version}`
        }
      })
      // return array of values
      return Object.values(productWithFormula)
    }
  },
  watch: {
    batches: {
      deep: true,
      handler (newVal, oldVal) {
        const keys = Object.keys(this.getTotalProductsInProduction())
        this.$nextTick(() => {
          keys.forEach((key) => this.matchupProductionWithOrder(key))
        })
      }
    }
  },
  methods: {
    saveBatchAndLotNumbers: function () {
      this.loaded = false
      if (!this.validateBatchesAndProductionRuns()) {
        this.loaded = true
        return
      }

      // Prepare request
      this.setBatchAndLotNumbers()
      this.order.sale_order_detail.forEach((detail, index) => {
        const saleOrderDetail = {
          so_detail_id: detail.so_detail_id,
          lot_num_assigned: true,
          timestamp_fetched: detail.timestamp_fetched,
          timestamp_modified: detail.timestamp_modified
        }
        this.req.upsertRecord('Sale_Order_Detail', saleOrderDetail)
      })
      const sale = {
        so_id: Number(this.id),
        lot_num_assigned: true,
        timestamp_fetched: this.order.timestamp_fetched,
        timestamp_modified: this.order.timestamp_modified
      }
      this.req.upsertRecord('Sales_Orders', sale)

      this.req.sendRequest(this.$root.getOrigin()).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status === 201) {
          this.$router.push({ path: `/orders/so/${this.id}` })
        } else {
          this.loaded = true
        }
      })
    },
    validateBatchesAndProductionRuns: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Batch/Production Assignment',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }
      const createToast = this.$root.createToast
      let valid = true

      this.batches.forEach((batch, index) => {
        if (!batch.product_with_formula_selected) {
          errorToast.message = `Batch #${index + 1} is missing a product with formula selection.`
          createToast(errorToast)
          valid = false
        }

        if (batch.productions.length < 1) {
          errorToast.message = `Batch #${index + 1} must have at least one production run.`
          createToast(errorToast)
          valid = false
        }

        if (batch.batch_size <= 0 || batch.batch_size === null || batch.batch_size === '') {
          errorToast.message = `Batch #${index + 1} Batch Size must be greater than 0.`
          createToast(errorToast)
          valid = false
        }

        if (batch.batch_requires_blending && (batch.max_blender_capacity <= 0 || batch.max_blender_capacity === null || batch.max_blender_capacity === '')) {
          errorToast.message = `Batch #${index + 1} Max Blender Capacity must be greater than 0.`
          createToast(errorToast)
          valid = false
        }

        if (batch.batch_requires_blending && batch.batch_size > batch.max_blender_capacity) {
          errorToast.message = `Batch #${index + 1} Batch Size must be less than or equal to the Max Blender Capacity.`
          createToast(errorToast)
          valid = false
        }

        if (batch.batch_allocated <= 0 || batch.batch_allocated === null || batch.batch_allocated === '') {
          errorToast.message = `Batch #${index + 1} Batch Allocated must be greater than 0.`
          createToast(errorToast)
          valid = false
        }

        if (batch.batch_remaining !== 0) {
          errorToast.message = `Batch #${index + 1} Batch Remaining must be equal to 0.`
          createToast(errorToast)
          valid = false
        }

        batch.productions.forEach((production, pindex) => {
          if (!production.variant) {
            errorToast.message = `Batch #${index + 1} Production #${pindex + 1} is missing a variant selection.`
            createToast(errorToast)
            valid = false
          }

          if (production.allocated_batch_size <= 0 || production.allocated_batch_size === null || production.allocated_batch_size === '') {
            errorToast.message = `Batch #${index + 1} Production #${pindex + 1} Allocated Batch Size must be greater than 0.`
            createToast(errorToast)
            valid = false
          }

          if (production.percent_loss <= 0 || production.percent_loss > 100) {
            errorToast.message = `Batch #${index + 1} Production #${pindex + 1} Percent Loss must be greater than 0 and less than or equal to 100.`
            createToast(errorToast)
            valid = false
          }

          if (production.target_unit_yield <= 0 || production.target_unit_yield === null || production.target_unit_yield === '') {
            errorToast.message = `Batch #${index + 1} Production #${pindex + 1} Target Unit Yield must be greater than 0.`
            createToast(errorToast)
            valid = false
          }
        })
      })

      this.checkOrder()
      if (!this.order.lot_num_assigned) {
        errorToast.message = 'Not all products have been assigned a batch and/or production run.'
        createToast(errorToast)
        valid = false
      }

      return valid
    },
    setBatchAndLotNumbers: function () {
      const lotAndBatchNumbers = []
      this.batches.forEach((batch) => {
        const lotAndBatchId = genTempKey()
        batch.productions.forEach((production, index) => {
          let orderIndex = null
          let soDetailId = null
          for (let i = 0; i < this.order.sale_order_detail.length; i++) {
            if (
              this.order.sale_order_detail[i].product_id === production.product_id &&
              this.order.sale_order_detail[i].formula_id === production.formula_id &&
              this.order.sale_order_detail[i].variant_id === production.variant_id
            ) {
              orderIndex = i
              break
            }
          }

          if (orderIndex !== null) {
            soDetailId = this.order.sale_order_detail[orderIndex].so_detail_id
          }
          if (index === 0) {
            const lotAndBatch = {
              lot_num_id: lotAndBatchId,
              so_detail_id: soDetailId,
              batch_record: true,
              total_batch_size: batch.batch_size,
              production_record: true,
              allocated_batch_size: production.allocated_batch_size,
              target_unit_yield: production.target_unit_yield,
              min_unit_yield: production.min_unit_yield,
              max_unit_yield: production.max_unit_yield,
              anticipated_loss_percent: production.percent_loss,
              timestamp_fetched: new Date().toISOString(),
              timestamp_modified: new Date().toISOString()
            }
            lotAndBatchNumbers.push(lotAndBatch)
          } else {
            const lot = {
              lot_num_id: genTempKey(),
              so_detail_id: soDetailId,
              batch_record: false,
              production_record: true,
              allocated_batch_size: production.allocated_batch_size,
              allocated_from_lot_num_id: lotAndBatchId,
              target_unit_yield: production.target_unit_yield,
              min_unit_yield: production.min_unit_yield,
              max_unit_yield: production.max_unit_yield,
              anticipated_loss_percent: production.percent_loss,
              timestamp_fetched: new Date().toISOString(),
              timestamp_modified: new Date().toISOString()
            }
            lotAndBatchNumbers.push(lot)
          }
        })
      })
      this.req = new CustomRequest(this.$cookies.get('session'))
      lotAndBatchNumbers.forEach((lotAndBatch) => {
        this.req.upsertRecord('Lot_And_Batch_Numbers', lotAndBatch)
      })
    },
    checkOrder: function () {
      this.order.sale_order_detail.forEach((detail, index) => {
        this.order.sale_order_detail[index].lot_num_assigned = false
      })
      this.order.lot_num_assigned = false
      const keys = Object.keys(this.getTotalProductsInProduction())
      keys.forEach((key) => this.matchupProductionWithOrder(key))
    },
    getTotalProductsInProduction: function () {
      const productionRuns = {}
      this.batches.forEach((batch) => {
        batch.productions.forEach((production) => {
          const key = `product_${batch.product_id}-formula_${batch.formula_id}-variant_${production.variant_id}`
          if (productionRuns[key]) {
            productionRuns[key].allocated_batch_size += batch.batch_allocated
            productionRuns[key].target_unit_yield += production.target_unit_yield
            productionRuns[key].min_unit_yield += production.min_unit_yield
            productionRuns[key].max_unit_yield += production.max_unit_yield
          } else {
            productionRuns[key] = {
              product_id: batch.product_id,
              formula_id: batch.formula_id,
              variant_id: production.variant_id,
              allocated_batch_size: batch.batch_allocated,
              percent_loss: production.percent_loss,
              target_unit_yield: production.target_unit_yield,
              min_unit_yield: production.min_unit_yield,
              max_unit_yield: production.max_unit_yield
            }
          }
        })
      })
      return productionRuns
    },
    matchupProductionWithOrder: function (key) {
      const prodInPro = this.getTotalProductsInProduction()
      const minProductionQty = prodInPro[key]?.min_unit_yield
      if (minProductionQty) {
        let orderIndex = null
        this.order.sale_order_detail.forEach((detail, index) => {
          if (
            detail.product_id === prodInPro[key].product_id &&
            detail.formula_id === prodInPro[key].formula_id &&
            detail.variant_id === prodInPro[key].variant_id
          ) {
            orderIndex = index
          }
        })

        if (orderIndex !== null) {
          this.order.sale_order_detail[orderIndex].lot_num_assigned = this.order.sale_order_detail[orderIndex].unit_order_qty <= minProductionQty
        }
      }

      let allLotsAssigned = true
      this.order.sale_order_detail.forEach((detail) => {
        if (!detail.lot_num_assigned) {
          allLotsAssigned = false
        }
      })
      this.order.lot_num_assigned = allLotsAssigned
    },
    validAllocation: function (production, batch) {
      return production.allocated_batch_size > 0 && production.allocated_batch_size !== null && production.allocated_batch_size !== '' && production.allocated_batch_size <= batch.max_blender_capacity
    },
    copyBatch: function (index) {
      const batch = cloneDeep(this.batches[index])
      this.batches.splice(index + 1, 0, batch)
      this.updateBatch(index + 1)
      this.checkOrder()
    },
    syncBatchWithAllocated: function (index, input) {
      if (!this.batches[index].multiple_variants) {
        if (input === 'production') {
          this.batches[index].batch_size = this.batches[index].productions[0].allocated_batch_size
        } else if (input === 'batch') {
          this.batches[index].productions[0].allocated_batch_size = this.batches[index].batch_size
        }
        this.calculateYield(index, this.batches[index].productions[0])
        this.$nextTick(() => {
          this.updateBatch(index)
        })
      }
    },
    calculateYield: function (index, production) {
      if (production.variant?.variant_type === 'powder') {
        // Target Unit Yield = (Allocated Batch Size * 1000) / Total Grams Per Unit
        const productionYield = (production.allocated_batch_size * 1000) / production.variant.total_grams_per_unit
        const loss = productionYield * (production.percent_loss / 100)
        production.target_unit_yield = Math.floor(productionYield - loss)

        // Min Unit Yield = (Allocated Batch Size * 1000) / Max Grams Per Unit
        const minProductionYield = (production.allocated_batch_size * 1000) / production.variant.max_grams_per_unit
        production.min_unit_yield = Math.floor(minProductionYield)
        if (productionYield - loss < minProductionYield) {
          production.min_unit_yield = Math.floor(productionYield - loss - 1)
        }

        // Max Unit Yield = (Allocated Batch Size * 1000) / Min Grams Per Unit
        const maxProductionYield = (production.allocated_batch_size * 1000) / production.variant.min_grams_per_unit
        production.max_unit_yield = Math.floor(maxProductionYield)
      } else if (production.variant?.variant_type === 'capsule') {
        // Target Unit Yield = (Allocated Batch Size * 1000000) / (Total Mg Per Capsule * Total Capsules Per Unit)
        const powderPerJar = production.variant.total_mg_per_capsule * production.variant.total_capsules_per_unit
        const productionYield = (production.allocated_batch_size * 1000000) / powderPerJar
        const loss = productionYield * (production.percent_loss / 100)
        production.target_unit_yield = Math.floor(productionYield - loss)

        // Min Unit Yield = (Allocated Batch Size * 1000000) / (Max Mg Per Capsule * Capsules Per Unit)
        const minPowderPerJar = production.variant.max_mg_per_capsule * production.variant.total_capsules_per_unit
        const minProductionYield = (production.allocated_batch_size * 1000000) / minPowderPerJar
        production.min_unit_yield = Math.floor(minProductionYield)
        if (productionYield - loss < minProductionYield) {
          production.min_unit_yield = Math.floor(productionYield - loss - 1)
        }

        // Max Unit Yield = (Allocated Batch Size * 1000000) / (Min Mg Per Capsule * Capsules Per Unit)
        const maxPowderPerJar = production.variant.min_mg_per_capsule * production.variant.total_capsules_per_unit
        const maxProductionYield = (production.allocated_batch_size * 1000000) / maxPowderPerJar
        production.max_unit_yield = Math.floor(maxProductionYield)
      } else if (production.variant?.variant_type === 'liquid') {
        // Target Unit Yield = (Allocated Batch Size * 1000) / Total Milliliters Per Unit
        const productionYield = production.allocated_batch_size * 1000 / production.variant.total_milliliters_per_unit
        const loss = productionYield * (production.percent_loss / 100)
        production.target_unit_yield = Math.floor(productionYield - loss)

        // Min Unit Yield = (Allocated Batch Size * 1000) / Max Milliliters Per Unit
        const minProductionYield = production.allocated_batch_size * 1000 / production.variant.max_milliliters_per_unit
        production.min_unit_yield = Math.floor(minProductionYield)
        if (productionYield - loss < minProductionYield) {
          production.min_unit_yield = Math.floor(productionYield - loss - 1)
        }

        // Max Unit Yield = (Allocated Batch Size * 1000) / Min Milliliters Per Unit
        const maxProductionYield = production.allocated_batch_size * 1000 / production.variant.min_milliliters_per_unit
        production.max_unit_yield = Math.floor(maxProductionYield)
      } else {
        production.target_unit_yield = 0
        production.min_unit_yield = 0
        production.max_unit_yield = 0
      }
      this.updateBatch(index)
    },
    updateBatch: function (index) {
      let totalAllocated = 0
      for (let i = 0; i < this.batches[index].productions.length; i++) {
        // convert allocated_batch_size to number
        totalAllocated += Number(this.batches[index].productions[i].allocated_batch_size)
      }
      this.batches[index].batch_allocated = Math.floor(totalAllocated * 100) / 100
      this.batches[index].batch_remaining = Math.ceil((this.batches[index].batch_size - totalAllocated) * 100) / 100

      this.$nextTick(() => {
        this.checkOrder()
      })
    },
    updateProduction: function (production, variant, index, pindex) {
      let percentLoss = 0
      if (variant.variant_type === 'powder') {
        percentLoss = 3
      } else if (variant.variant_type === 'capsule') {
        percentLoss = 5
      } else if (variant.variant_type === 'liquid') {
        percentLoss = 3
      }
      const update = {
        ...production,
        variant: variant,
        variant_id: variant.variant_id,
        percent_loss: percentLoss
      }
      this.batches[index].productions[pindex] = update
      this.calculateYield(index, update)
      this.updateBatch(index)
      return update
    },
    getVariants: function (batch) {
      const variants = []
      batch.productions_allowed.forEach((production) => {
        const variant = production.variant[0]
        variant.percent_loss = production.percent_loss
        variants.push(variant)
      })
      return variants
    },
    deleteProductionRun: function (index, pindex) {
      this.batches[index].productions.splice(pindex, 1)
      this.order.sale_order_detail.forEach((detail, index) => {
        this.order.sale_order_detail[index].lot_num_assigned = false
      })
      this.order.lot_num_assigned = false
      this.updateBatch(index)
    },
    addProductionRun: function (index) {
      this.batches[index].productions.push({
        target_unit_yield: 0.0,
        min_unit_yield: 0.0,
        max_unit_yield: 0.0,
        allocated_batch_size: 0.0,
        production_record: true,
        percent_loss: 0.0
      })
      this.checkOrder()
    },
    getProductionsAllowed: function (index) {
      const productId = this.batches[index].product_id
      const formulaId = this.batches[index].formula_id

      this.order.sale_order_detail.forEach((detail) => {
        if (detail.product_id === productId && detail.formula_id === formulaId) {
          this.batches[index].productions_allowed.push(cloneDeep(detail))
        }
      })
    },
    selectProductWithFormula: function (index, productWithFormula) {
      this.batches[index].product = productWithFormula.product
      this.batches[index].product_id = productWithFormula.product_id
      this.batches[index].formula = productWithFormula.formula
      this.batches[index].formula_id = productWithFormula.formula_id
      this.batches[index].title = productWithFormula.title

      if (productWithFormula.product_id && productWithFormula.formula_id) {
        this.batches[index].product_with_formula_selected = true
      } else {
        this.batches[index].product_with_formula_selected = false
      }
      this.getProductionsAllowed(index)
    },
    deleteBatch: function (index) {
      this.batches.splice(index, 1)
      this.checkOrder()
    },
    addBatch: function () {
      this.batches.push({
        product_id: null,
        product: {},
        formula_id: null,
        formula: {},
        title: null,
        productions_allowed: [],
        productions: [
          {
            target_unit_yield: 0.0,
            min_unit_yield: 0.0,
            max_unit_yield: 0.0,
            allocated_batch_size: 0,
            production_record: true,
            percent_loss: 0
          }
        ],
        product_with_formula_selected: false,
        batch_size: 0,
        batch_requires_blending: true,
        multiple_variants: false,
        batch_allocated: 0.0,
        batch_remaining: 0.0,
        batch_type: 'Powder',
        max_blender_capacity: 312.0
      })
    },
    toggleAssignLotNumbers: function () {
      this.assign_lot_numbers_mode = !this.assign_lot_numbers_mode
    },
    handleVisible: function (isVisible) {
      this.isMd = isVisible
    },
    saveDocs: function () {
      this.order.doc.sale_order_files = cloneDeep(this.sale_order_files_buffer)
      this.edit_documents = false
    },
    toggleEditDocs: function () {
      if (!this.edit_documents) {
        this.sale_order_files_buffer = cloneDeep(this.order.doc.sale_order_files)
      }
      this.edit_documents = !this.edit_documents
    },
    getSale: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/orders/sales?populate=sale_order_detail&populate=client&doc=true&so_id=' + this.id
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
            this.order = data.data[0]
            this.sale_order_files_buffer = cloneDeep(this.order.doc.sale_order_files)
            this.loaded = true
            // eslint-disable-next-line
            console.log(data.data)
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
    },
    getFile: function (document) {
      if (document.file_hash) {
        const url = this.$root.getOrigin() + '/api/v1/uploads/' + document.file_pointer
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
    addDocument: function (documents) {
      const document = {
        id: genTempKey(),
        description: null,
        name: null,
        type: `orders/so/${this.order.client[0].organization_name}/${this.order.client_po}/`,
        id_code: `${this.order.client_po}_`,
        file_pointer: null,
        file_preview_pointer: null,
        file_type: null,
        url_preview: null,
        file_hash: null,
        date_uploaded: null
      }
      documents.push(document)
    }
  },
  created: function () {
    this.getSale()
  }
}
</script>

<style scoped>
.custom_card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}
.my_component {
    width: 90%;
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
</style>
