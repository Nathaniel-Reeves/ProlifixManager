<template>
 <div class="my_component">
    <div v-if="!loaded" class="d-flex justify-content-center">
      <div class="card my-2" style="box-shadow: 0 20px 40px rgba(0,0,0,.2); max-width:fit-content;">
        <div class="card-body">
          <div class="d-flex justify-content-center">
            <div class="spinner-border text-primary" role="status"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="card my-2" v-else>
      <div class="card-body">
        <h2 class="card-title flex-grow-1" v-if="!client_selected">New Sale</h2>
        <h2 v-if="client_selected">
          New <router-link class="text-info" :to="'/organizations/'+selected_client.organization_id" target="_blank">{{ selected_client.organization_primary_name }}</router-link> Order
        </h2>
        <b-form>
          <b-container class="my-3" v-if="!client_selected">
            <b-row class="mb-2">
              <b-col md="1">
                <span>Client: </span>
              </b-col>
              <b-col class="d-flex flex-row flex-nowrap">
                <ChooseOrg :organizations="clients" :selected="selected_client_buffer" @org="(o) => selected_client_buffer = o" :org-req="true" :disabled-prop="client_selected" :initial="false"></ChooseOrg>
              </b-col>
            </b-row>
          </b-container>
          <div class="m-3" v-if="!client_selected">
            <b-button block variant="outline-success" @click="setClient()" :disabled="!selected_client_buffer?.organization_id">Continue</b-button>
          </div>
          <div v-if="!client_selected" class="d-flex justify-content-center">
            <p>Select the client before moving forward with order details.</p>
          </div>
          <div v-else>
            <div class="d-flex justify-content-center" v-if="products.length === 0">
              <div class="spinner-border text-primary" role="status"></div>
            </div>
            <div v-else>
              <b-container class="my-3">
                <b-row class="mb-2">
                  <b-col md="3">
                    <span>Client PO: </span>
                  </b-col>
                  <b-col>
                    <div class="input-group">
                      <b-form-input v-model="order_buffer.client_po"
                        aria-describedby="client_po-live-feedback"
                        :class="[(order_buffer.client_po.length > 0 ? '' : 'is-invalid')]"
                      ></b-form-input>
                      <div id="client_po-live-feedback" class="invalid-feedback">This is a required field.</div>
                    </div>
                  </b-col>
                </b-row>
                <b-row class="mb-2">
                  <b-col md="3">
                    <span>Date Ordered: </span>
                  </b-col>
                  <b-col>
                    <b-form-datepicker
                      id="order_date"
                      v-model="order_buffer.order_date"
                      :max="new Date()"
                    ></b-form-datepicker>
                  </b-col>
                </b-row>
                <b-row class="mb-2">
                  <b-col md="3">
                    <span>Target Completion Date: </span>
                  </b-col>
                  <b-col>
                    <b-form-datepicker
                      id="target_completion_date"
                      v-model="order_buffer.target_completion_date"
                      :min="order_buffer.order_date"
                      :state="order_buffer.target_completion_date < order_buffer.order_date ? false : null"
                    ></b-form-datepicker>
                  </b-col>
                </b-row>
              </b-container>
              <b-card-group class="d-flex flex-column">
                <div v-for="selected_product, index in selected_products" :key="index">
                  <b-card class="custom_card mb-2" style="width: 100%;" no-body>
                    <b-card-title class="m-3 d-flex justify-content-between">
                      <div v-if="selected_product.product_and_formula_selected" class="m-2 d-flex flex-row">
                        <router-link class="mr-2 mt-2" :to="'/catalogue/products/'+selected_product.product_id" target="_blank">
                          <h3 class="m-0 text-info">{{ selected_product.product.product_name }} V{{ selected_product.formulation_version }}</h3>
                        </router-link>
                        <h6><CertBadge :data="selected_product.product"></CertBadge></h6>
                      </div>
                      <div v-if="selected_product.product_and_formula_selected">
                        <b-button variant="outline-danger" class="text-nowrap" @click="removeRow(index)">Remove Product</b-button>
                      </div>
                    </b-card-title>
                    <b-card-body>
                      <b-container v-if="!selected_product.product_and_formula_selected">
                        <b-row class="mb-2">
                          <b-col md="2">
                            <span><strong>Product: </strong></span>
                          </b-col>
                          <b-col class="d-flex flex-row flex-nowrap">
                            <ChooseProduct :products="products" :selected="selected_product.product" @product="(p) => selectProduct(index, p)" :disabled-prop="false" :product-req="true"></ChooseProduct>
                          </b-col>
                        </b-row>
                        <b-row class="mb-2" v-if="selected_products[index].formulas?.length > 0">
                          <b-col md="2">
                            <span><strong>Formula: </strong></span>
                          </b-col>
                          <b-col class="d-flex flex-row flex-nowrap">
                            <ChooseFormula :primary-formula-id="selected_product.default_formula_id" :formulas="selected_product.formulas" :selected="selected_product.selected_formula" @formula="(f) => selectFormula(index, f)" :disabled-prop="false" :formula-req="true"></ChooseFormula>
                          </b-col>
                        </b-row>
                      </b-container>
                      <b-container v-if="selected_product.product_and_formula_selected" fluid>
                        <b-row class="my-1">
                          <b-col>
                            <strong>Variant</strong>
                          </b-col>
                          <b-col>
                            <strong>Qty</strong>
                          </b-col>
                          <b-col>
                            <strong>Unit Price</strong>
                          </b-col>
                          <b-col>
                            <strong>Percent Overage</strong>
                          </b-col>
                          <b-col>
                            <strong>Special Instructions</strong>
                          </b-col>
                          <b-col>
                            <strong>Estimated Bulk Qty</strong>
                          </b-col>
                        </b-row>
                        <hr class="mb-2">
                        <div v-for="variant, vindex in selected_product.selected_variants" :key="vindex">
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
                                <div class="input-group-prepend">
                                  <span class="input-group-text">$</span>
                                </div>
                                <b-form-input v-model="variant.bid_price_per_unit" type="number"
                                  aria-describedby="bid_price_per_unit-live-feedback"
                                  :class="[(variant.bid_price_per_unit >= 0 && variant.bid_price_per_unit !== null ? '' : 'is-invalid')]"
                                ></b-form-input>
                                <div id="bid_price_per_unit-live-feedback" class="invalid-feedback">This required field must be greater than 0.</div>
                              </div>
                            </b-col>
                            <b-col>
                              <div class="input-group">
                                <b-form-input v-model="variant.percent_overage" type="number"
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
                                {{ calcBulkPowder(variant) }} kg
                              </div>
                              <div v-else-if="variant.variant_type === 'capsule'">
                                {{ calcBulkCapsule(variant) }} kg
                              </div>
                              <div v-else-if="variant.variant_type === 'liquid'">
                                {{ calcBulkLiquid(variant) }} L
                              </div>
                            </b-col>
                          </b-row>
                          <hr class="mb-2">
                        </div>
                      </b-container>
                      <!-- <div class="m-3">
                        <b-button block variant="outline-info" @click="addVariant(index)" v-if="selected_product.product_and_formula_selected">Add Variant</b-button>
                      </div> -->
                    </b-card-body>
                  </b-card>
                </div>
                <b-card id="add-product" class="custom_card mb-2" style="width: 100%;cursor: pointer;" no-body @click="addRow()">
                  <b-card-body class="d-flex justify-content-center align-items-center">
                    <b-icon icon="plus-lg" size="2rem"></b-icon>
                    <b class="ml-2">Add Product</b>
                  </b-card-body>
                </b-card>
                <b-tooltip target="add-product" triggers="hover">Add Product to Order</b-tooltip>
              </b-card-group>
              <div class="d-print-none">
                <h3 id="Documents">Documents</h3>
                <b-card-group class="ml-3">
                  <div v-for="(document, index) in documents" :key="index">
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
                        <strong>Document Name: </strong><br><b-form-input v-model="document.name" type="text" class="my-1"></b-form-input>
                        <strong>Description: </strong><br><b-form-textarea v-model="document.description" class="my-1" rows="3" max-rows="3"></b-form-textarea>
                        <b-form-file v-if="!document.file_hash" :disabled="!document.document_type || !document.name" no-drop accept="image/png, image/jpeg, application/pdf" type="file" class="my-2" @change="onFileChange($event, document)"></b-form-file>
                        <b-button :disabled="!document.document_type || !document.name || !document.file_pointer" block :href="getFile(document)" target="_blank" class="btn-light">View Document</b-button>
                      </b-card-body>
                      <b-card-footer>
                        <b-button block :disabled="!document.document_type || !document.name" variant="outline-danger" @click="deleteDocument(document)">Delete Document</b-button>
                      </b-card-footer>
                    </b-card>
                  </div>
                  <b-card class="m-2 custom_card" style="min-width: 22rem; max-width: 22rem; cursor: pointer;" @click="addDocument()">
                    <b-card-title>Add Document</b-card-title>
                  </b-card>
                </b-card-group>
              </div>
              <div class="mt-3">
                <b-button :disabled="!(selected_products.length > 0 && selected_products[0].selected_variants.length > 0)" class="mr-2" variant="outline-success" @click="saveOrder()">Save</b-button>
                <b-button variant="outline-danger" to="/orders/so">Cancel</b-button>
              </div>
            </div>
          </div>
        </b-form>
      </div>
    </div>
 </div>
</template>

<style scoped>
.custom_card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}
.my_component {
    width: 80%;
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

<script>
import CertBadge from '@/components/CertBadge.vue'
import ChooseOrg from '@/components/ChooseOrg.vue'
import ChooseProduct from '@/components/ChooseProduct.vue'
import ChooseFormula from '@/components/ChooseFormula.vue'
import ChooseVariant from '@/components/ChooseVariant.vue'
import { CustomRequest, genTempKey } from '../../../common/CustomRequest.js'
import vSelect from 'vue-select'

export default {
  name: 'NewSalesOrder',
  components: {
    CertBadge,
    ChooseOrg,
    ChooseProduct,
    ChooseFormula,
    ChooseVariant,
    vSelect
  },
  data: function () {
    return {
      clients: [],
      force_loaded: true,
      selected_client_buffer: null,
      selected_client: null,
      client_selected: false,
      products: [],
      selected_products: [],
      documents: [],
      order_buffer: {
        order_date: new Date(),
        target_completion_date: new Date(new Date().setMonth(new Date().getMonth() + 3)),
        client_po: ''
      },
      req: new CustomRequest(this.$cookies.get('session')),
      del_url_previews: []
    }
  },
  computed: {
    loaded: function () {
      if (this.force_loaded) {
        return this.clients.length > 0
      }
      return false
    }
  },
  methods: {
    calcBulkCapsule: function (variant) {
      const totalPowderInKg = Math.ceil((variant.total_mg_per_capsule / 1000 * variant.total_capsules_per_unit) * variant.qty / 1000)
      const overage = Math.ceil(totalPowderInKg * (variant.percent_overage / 100))
      const out = totalPowderInKg + overage
      if (out) {
        return out
      }
      return 0
    },
    calcBulkPowder: function (variant) {
      const totalPowderInKg = Math.ceil(variant.total_grams_per_unit * variant.qty / 1000)
      const overage = Math.ceil(totalPowderInKg * (variant.percent_overage / 100))
      const out = totalPowderInKg + overage
      if (out) {
        return out
      }
      return 0
    },
    calcBulkLiquid: function (variant) {
      const totalLiquidInL = Math.ceil(variant.total_milliliters_per_unit * variant.qty / 1000)
      const overage = Math.ceil(totalLiquidInL * (variant.percent_overage / 100))
      const out = totalLiquidInL + overage
      if (out) {
        return out
      }
      return 0
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
    deleteDocument: function (document) {
      this.documents.splice(this.documents.findIndex((d) => d.id === document.id), 1)
      this.req.deleteFile(document.file_pointer)
    },
    addDocument: function () {
      const document = {
        id: genTempKey(),
        description: null,
        name: null,
        type: `orders/so/${this.selected_client.organization_primary_name}/${this.order_buffer.client_po}/`,
        id_code: `${this.order_buffer.client_po}_`,
        file_pointer: null,
        file_preview_pointer: null,
        file_type: null,
        url_preview: null,
        file_hash: null,
        date_uploaded: null
      }
      this.documents.push(document)
    },
    validateOrder: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Order',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }
      const createToast = this.$root.createToast
      let valid = true

      if (this.order_buffer.client_po.length === 0) {
        errorToast.message = 'Client PO is a required field.'
        createToast(errorToast)
        valid = false
      }

      if (this.order_buffer.target_completion_date < this.order_buffer.order_date) {
        errorToast.message = 'Target Completion Date must be after the Order Date.'
        createToast(errorToast)
        valid = false
      }

      if (this.selected_products.length === 0) {
        errorToast.message = 'At least one product must be selected.'
        createToast(errorToast)
        valid = false
      }

      // must upload at least one document
      let hasDocument = false
      for (let i = 0; i < this.documents.length; i++) {
        if (this.documents[i].file_pointer) {
          hasDocument = true
          break
        }
      }
      if (!hasDocument) {
        errorToast.message = 'At least one document must be uploaded.'
        createToast(errorToast)
        valid = false
      }

      for (let i = 0; i < this.selected_products.length; i++) {
        if (!this.selected_products[i].product_and_formula_selected) {
          errorToast.message = 'All products must have a product and formula selected.'
          createToast(errorToast)
          valid = false
        }
        if (this.selected_products[i].selected_variants.length === 0) {
          errorToast.message = 'All products must have at least one variant selected.'
          createToast(errorToast)
          valid = false
        }
        for (let j = 0; j < this.selected_products[i].selected_variants.length; j++) {
          if (!this.selected_products[i].selected_variants[j]?.variant_id || this.selected_products[i].selected_variants[j].variant_id === null) {
            errorToast.message = 'All variants must have a variant selected.'
            createToast(errorToast)
            valid = false
            break
          }
          if (this.selected_products[i].selected_variants[j].qty === null || this.selected_products[i].selected_variants[j].qty <= 0) {
            errorToast.message = 'All variants must have a quantity greater than 0.'
            createToast(errorToast)
            valid = false
            break
          }
          if (this.selected_products[i].selected_variants[j].bid_price_per_unit === null || this.selected_products[i].selected_variants[j].bid_price_per_unit <= 0) {
            errorToast.message = 'All variants must have a bid price per unit greater than 0.'
            createToast(errorToast)
            valid = false
            break
          }
          if (this.selected_products[i].selected_variants[j].percent_overage === null || this.selected_products[i].selected_variants[j].percent_overage < 0) {
            errorToast.message = 'All variants must have a percent overage greater than or equal to 0.'
            createToast(errorToast)
            valid = false
            break
          }
        }
        if (!valid) {
          break
        }
      }

      return valid
    },
    saveOrder: function () {
      this.force_loaded = false
      if (!this.validateOrder()) {
        this.force_loaded = true
        return
      }

      // Prepare request
      const saleOrderId = genTempKey()
      let theoreticalPOAmount = 0

      for (let i = 0; i < this.selected_products.length; i++) {
        const product = this.selected_products[i]
        for (let j = 0; j < product.selected_variants.length; j++) {
          const saleOrderDetail = {
            so_detail_id: genTempKey(),
            so_id: saleOrderId,
            product_id: product.product_id,
            formula_id: product.formula_id,
            variant_id: product.selected_variants[j].variant_id,
            unit_order_qty: product.selected_variants[j].qty,
            percent_overage: product.selected_variants[j].percent_overage,
            special_instructions: product.selected_variants[j].special_instructions,
            bid_price_per_unit: product.selected_variants[j].bid_price_per_unit,
            timestamp_fetched: new Date().toISOString()
          }
          this.req.upsertRecord('Sale_Order_Detail', saleOrderDetail)
          theoreticalPOAmount += product.selected_variants[j].bid_price_per_unit * product.selected_variants[j].qty
        }
      }

      const saleOrder = {
        so_id: saleOrderId,
        organization_id: this.selected_client.organization_id,
        client_po_num: this.order_buffer.client_po,
        order_date: new Date(this.order_buffer.order_date).toISOString().split('T')[0],
        target_completion_date: new Date(this.order_buffer.target_completion_date).toISOString().split('T')[0],
        timestamp_fetched: new Date().toISOString(),
        theoretical_po_amount: theoreticalPOAmount,
        doc: {
          sale_order_files: this.documents
        }
      }
      this.req.upsertRecord('Sales_Orders', saleOrder)

      this.req.sendRequest(this.$root.getOrigin()).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status === 201) {
          Object.values(resp.data[0].temp_key_lookup).forEach(item => {
            if (item.table_name === 'Sales_Orders') {
              this.$router.push({ path: `/orders/so/${item.new_id}` })
            }
          })
        }
      })

      this.force_loaded = true
    },
    updateVariant: function (variant, v, index, vindex) {
      const update = {
        ...variant,
        ...v
      }
      if (update.variant_type === 'powder') {
        update.percent_overage = 3
      }
      if (update.variant_type === 'capsule') {
        update.percent_overage = 5
      }
      this.selected_products[index].selected_variants.splice(vindex, 1, update)
      return update
    },
    addVariant: function (index) {
      this.selected_products[index].selected_variants.push({
        qty: null,
        percent_overage: null,
        bid_price_per_unit: null,
        special_instructions: '',
        variant_id: null,
        variant_title: ''
      })
    },
    finishProductSelection: function (index) {
      this.selected_products[index].product_and_formula_selected = true
    },
    selectFormula: function (index, formula) {
      this.selected_products[index].selected_formula = formula
      this.selected_products[index].formula_id = formula.formula_id
      this.selected_products[index].formulation_version = formula.formulation_version
      this.finishProductSelection(index)
    },
    selectProduct: function (index, product) {
      this.selected_products[index].product = product
      this.selected_products[index].product_id = product.product_id
      this.selected_products[index].variants = product.product_variants
      this.selected_products[index].formulas = product.formulas
      this.selected_products[index].default_formula_id = product.default_formula_id
    },
    removeRow: function (index) {
      this.selected_products.splice(index, 1)
    },
    addRow: function () {
      this.selected_products.push({
        product_id: null,
        product: {},
        selected_formula: null,
        variants: [],
        selected_variants: [
          {
            qty: null,
            percent_overage: null,
            bid_price_per_unit: null,
            special_instructions: '',
            variant_id: null,
            variant_title: ''
          }
        ],
        formulas: [],
        formula_id: null,
        formulation_version: null,
        default_formula_id: null,
        product_and_formula_selected: false
      })
    },
    getProducts: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/catalogue/products?client-id=' + this.selected_client.organization_id + '&product-type=product&populate=formulas&populate=product_variants'
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
            this.products = data.data
            // eslint-disable-next-line
            console.log(this.products)
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else if (response.status === 404) {
          const createToast = this.$root.createToast
          const message = {
            title: 'No Products Found',
            message: 'No products found for this client. Please add products to the client before creating an order.',
            variant: 'danger'
          }
          createToast(message)
          this.selected_client = null
          this.client_selected = false
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
          console.log(response)
        }
      })
    },
    setClient: function () {
      this.selected_client = this.selected_client_buffer
      this.client_selected = true
      this.getProducts()
    },
    getClients: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/organizations?org-type=client'
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
            this.clients = data.data
            // eslint-disable-next-line
            console.log(this.clients)
          })
        } else if (response.status === 401) {
          this.$router.push({
            name: 'login'
          })
        } else if (response.status === 404) {
          const createToast = this.$root.createToast
          const message = {
            title: 'No Clients Found',
            message: 'No clients found. Please add clients before creating an order.',
            variant: 'danger'
          }
          createToast(message)
        } else {
          // eslint-disable-next-line
          console.log('Looks like there was a problem. Status Code:' + response.status)
          // eslint-disable-next-line
          console.log(response)
        }
      })
    }
  },
  created: function () {
    this.getClients()
  }
}
</script>
