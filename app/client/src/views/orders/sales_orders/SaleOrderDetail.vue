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
                    <b-button @click="toggleAssignLotNumbers()" v-if="!order.lot_num_assigned" class="mr-2 mb-2" variant="outline-primary" :block="isMd">Assign Lot Numbers</b-button>
                    <b-badge v-if="!order.lot_num_assigned" variant="warning" class="p-2" :block="isMd">
                      <b-icon icon="exclamation-triangle-fill"></b-icon> Lot Number Assignment Incomplete
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
            <h4>Order Details<b-button @click="toggleAssignLotNumbers()" v-if="!order.lot_num_assigned" v-show="!assign_lot_numbers_mode" class="ml-2" variant="outline-primary">Assign Lot Numbers</b-button></h4>
            <OrderDetailsTable :order-details="order.sale_order_detail"></OrderDetailsTable>
            <b-card-group class="d-flex flex-column">
              <div v-for="batch, index in batches" :key="index">
                <b-card class="custom_card mb-2" style="width: 100%;" no-body>
                  <b-card-title class="m-3 d-flex justify-content-between">
                    <div v-if="batch.product_with_formula_selected" class="m-2 d-flex flex-row">
                      <h3 class="m-0">Batch #{{ index + 1 }}:
                        <router-link class="mr-2 mt-2 text-info" :to="'/catalogue/products/'+batch.product_id" target="_blank">
                          {{ batch.title }}
                        </router-link>
                      </h3>
                      <h6><CertBadge :data="batch.product[0]"></CertBadge></h6>
                    </div>
                    <div v-if="batch.product_with_formula_selected">
                      <b-button variant="outline-danger" class="text-nowrap" @click="removeRow(index)">Remove Batch</b-button>
                    </div>
                  </b-card-title>
                  <b-card-body>
                    <b-container v-if="!batch.product_with_formula_selected">
                      <b-row class="mb-2">
                        <b-col md="2">
                          <span><strong>Batch for Product: </strong></span>
                        </b-col>
                        <b-col class="d-flex flex-row flex-nowrap">
                          <ChooseProductWithFormula :products-with-formulas="product_with_formula_menu" :selected="batch" @product-with-formula="(pwf) => selectProductWithFormula(index, pwf)" :disabled="false" :product-req="true"></ChooseProductWithFormula>
                        </b-col>
                      </b-row>
                    </b-container>
                    <b-container v-if="batch.product_with_formula_selected" fluid>
                      <b-row align-v="center">
                        <b-col md="3" class="mb-2" align-v="center">
                          <b>Blending Required: </b>
                          <div class="d-flex justify-content-center">
                            <b-button @click="batch.batch_requires_blending = false" v-show="batch.batch_requires_blending" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                            <b-button @click="batch.batch_requires_blending = true" v-show="!batch.batch_requires_blending" class="badge badge-danger badge-pill" style="font-size: 1.5em;">No</b-button>
                          </div>
                        </b-col>
                        <b-col md="3" class="mb-2">
                          <b>Batch Type:</b>
                          <v-select v-model="batch.batch_type" required label="text" :reduce="doc => doc.value" placeholder="Batch Type"
                          :options="[
                            { value: 'Powder', text: 'Powder' },
                            { value: 'Liquid', text: 'Liquid' }
                          ]">
                          </v-select>
                        </b-col>
                        <b-col md="3" class="mb-2">
                          <b>Batch Size: </b>
                          <div class="input-group">
                            <b-form-input v-model="batch.batch_size" type="number"
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
                    <!-- <b-container v-if="selected_product.product_and_formula_selected">
                      <b-row class="my-1">
                        <b-col>
                          <strong>Variant</strong>
                        </b-col>
                        <b-col>
                          <strong>Qty</strong>
                        </b-col>
                        <b-col>
                          <strong>Percent Overage</strong>
                        </b-col>
                        <b-col>
                          <strong>Bulk Qty</strong>
                        </b-col>
                      </b-row>
                      <hr class="mb-2">
                      <div v-for="production, vindex in batch.productions" :key="vindex">
                        <b-row class="my-1">
                          <b-col>
                            <ChooseVariant :variants="selected_product.variants" :selected="variant" @variant="(v) => variant = updateVariant(variant, v, index, vindex)" :disabled-prop="false" :variant-req="true"></ChooseVariant>
                          </b-col>
                          <b-col>
                            <div class="input-group">
                              <b-form-input v-model="variant.qty" type="number"
                                aria-describedby="qty-live-feedback"
                                :class="[(variant.qty > 0 ? '' : 'is-invalid')]"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span class="input-group-text">ct</span>
                              </div>
                              <div id="qty-live-feedback" class="invalid-feedback">This required field must be between greater than 0.</div>
                            </div>
                          </b-col>
                          <b-col>
                            <div class="input-group">
                              <b-form-input v-model="variant.percent_overage" type="number"
                                disabled
                                aria-describedby="percent_overage-live-feedback"
                                :class="[(variant.percent_overage >= 0 && variant.percent_overage !== null && variant.percent_overage !== '' && variant.percent_overage <= 100 ? '' : 'is-invalid')]"
                              ></b-form-input>
                              <div class="input-group-append">
                                <span class="input-group-text">%</span>
                              </div>
                              <div id="percent_overage-live-feedback" class="invalid-feedback">This required field must be between 0 and 100.</div>
                            </div>
                          </b-col>
                          <b-col>
                            <div>
                              <b-textarea v-model="variant.special_instructions" rows="1" max-rows="6"></b-textarea>
                            </div>
                          </b-col>
                          <b-col class="mt-2">
                            <div v-if="variant.variant_type === 'powder'">
                              {{ Math.ceil((variant.total_grams_per_unit * variant.qty) / 1000) + (Math.ceil((variant.total_grams_per_unit * variant.qty) / 1000) * (variant.percent_overage / 100)) }} kg
                            </div>
                            <div v-else-if="variant.variant_type === 'capsule'">
                              {{ Math.ceil((variant.total_mg_per_capsule * variant.total_capsules_per_unit * variant.qty) / 1000000) + (Math.ceil((variant.total_mg_per_capsule * variant.total_capsules_per_unit * variant.qty) / 1000000) * (variant.percent_overage / 100)) }} kg
                            </div>
                            <div v-else-if="variant.variant_type === 'liquid'">
                              {{ Math.ceil((variant.total_milliliters_per_unit * variant.qty) / 1000) + (Math.ceil((variant.total_milliliters_per_unit * variant.qty) / 1000) * (variant.percent_overage / 100)) }} L
                            </div>
                          </b-col>
                        </b-row>
                        <hr class="mb-2">
                      </div>
                    </b-container>
                    <div class="m-3">
                      <b-button block variant="outline-info" @click="addVariant(index)" v-if="selected_product.product_and_formula_selected">Add Variant</b-button>
                    </div> -->
                  </b-card-body>
                </b-card>
              </div>
              <b-card id="add-product" class="custom_card mb-2" style="width: 100%;cursor: pointer;" no-body @click="addRow()">
                <b-card-body class="d-flex justify-content-center">
                  <!-- <b-icon icon="plus-lg" size="2rem"></b-icon> -->
                   <b>Add a Batch</b>
                </b-card-body>
              </b-card>
              <b-tooltip target="add-product" triggers="hover">Add Product to Order</b-tooltip>
            </b-card-group>
            <pre>{{ JSON.stringify(order, null, 4) }}</pre>
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
import CertBadge from '@/components/CertBadge.vue'

export default {
  name: 'SaleOrderDetail',
  components: {
    vSelect,
    OrderDetailsTable,
    ChooseProductWithFormula,
    CertBadge
  },
  data: function () {
    return {
      loaded: false,
      id: this.$route.params.id,
      edit_documents: false,
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
  methods: {
    getProductionsAllowed: function (index) {
      const productId = this.batches[index].product_id
      const formulaId = this.batches[index].formula_id

      this.order.sale_order_detail.forEach((detail) => {
        if (detail.product_id === productId && detail.formula_id === formulaId) {
          this.batches[index].productions_allowed = cloneDeep(detail)
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
    removeRow: function (index) {
      this.batches.splice(index, 1)
    },
    addRow: function () {
      this.batches.push({
        product_id: null,
        product: null,
        formula_id: null,
        formula: null,
        title: null,
        productions_allowed: [],
        productions: [],
        product_with_formula_selected: false,
        batch_size: 300,
        batch_requires_blending: true,
        batch_allocated: 0,
        batch_remaining: 0,
        batch_type: 'Powder'
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
