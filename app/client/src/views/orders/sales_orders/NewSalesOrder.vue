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
        <h2 v-if="client_selected">New {{ selected_client.organization_primary_name }} Order</h2>
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
                    <b-form-input v-model="order_buffer.client_po"></b-form-input>
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
                      :max="new Date()"
                    ></b-form-datepicker>
                  </b-col>
                </b-row>
              </b-container>
              <b-card-group class="d-flex flex-column">
                <div v-for="selected_product, index in selected_products" :key="index">
                  <b-card class="custom_card mb-2" style="width: 100%;" no-body>
                    <b-card-title class="m-3 d-flex justify-content-between">
                      <div v-if="selected_product.product_and_formula_selected" class="m-2 d-flex flex-row">
                        <div class="mr-2 mt-2">
                          <h3 class="m-0">{{ selected_product.product.product_name }} V{{ selected_product.formulation_version }}</h3>
                        </div>
                        <h6><CertBadge :data="selected_product.product"></CertBadge></h6>
                      </div>
                      <div v-if="selected_product.product_and_formula_selected">
                        <b-button variant="outline-danger" class="text-nowrap" @click="removeRow(index)">Remove Product</b-button>
                      </div>
                    </b-card-title>
                    <b-card-body>
                      <b-container v-if="!selected_product.product_and_formula_selected">
                        <b-row class="mb-2">
                          <b-col md="3">
                            <span><strong>Product: </strong></span>
                          </b-col>
                          <b-col class="d-flex flex-row flex-nowrap">
                            <ChooseProduct :products="products" :selected="selected_product.product" @product="(p) => selectProduct(index, p)" :disabled-prop="false"></ChooseProduct>
                          </b-col>
                        </b-row>
                        <b-row class="mb-2" v-if="selected_products[index].formulas.length > 0">
                          <b-col md="3">
                            <span><strong>Formula: </strong></span>
                          </b-col>
                          <b-col class="d-flex flex-row flex-nowrap">
                            <ChooseFormula :formulas="selected_product.formulas" :selected="selected_product.selected_formula" @formula="(f) => selectFormula(index, f)" :disabled-prop="false"></ChooseFormula>
                          </b-col>
                        </b-row>
                      </b-container>
                      <hr v-if="selected_product.product_and_formula_selected">
                      <b-container v-if="selected_product.product_and_formula_selected">
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
                            <strong>Special Instructions</strong>
                          </b-col>
                        </b-row>
                        <div v-for="variant, vindex in selected_product.selected_variants" :key="vindex">
                          <b-row class="my-1">
                            <b-col>
                              <ChooseVariant :variants="selected_product.variants" :selected="variant" @variant="(v) => variant = {...v, variant}" :disabled-prop="false"></ChooseVariant>
                            </b-col>
                            <b-col>
                              <b-form-input v-model="variant.qty" type="number"></b-form-input>
                            </b-col>
                            <b-col>
                              <b-form-input v-model="variant.percent_overage" type="number"></b-form-input>
                            </b-col>
                            <b-col>
                              <b-form-input v-model="variant.special_instructions"></b-form-input>
                            </b-col>
                          </b-row>
                        </div>
                      </b-container>
                      <div class="m-3">
                        <b-button block variant="outline-info" @click="addVariant(index)" v-if="selected_product.product_and_formula_selected">Add Variant</b-button>
                      </div>
                    </b-card-body>
                  </b-card>
                </div>
                <b-card id="add-product" class="custom_card mb-2" style="width: 100%;cursor: pointer;" no-body @click="addRow()">
                  <b-card-body class="d-flex justify-content-center">
                    <b-icon icon="plus-lg" size="2rem"></b-icon>
                  </b-card-body>
                </b-card>
                <b-tooltip target="add-product" triggers="hover">Add Product to Order</b-tooltip>
              </b-card-group>
              <div class="mt-3">
                <b-button :disabled="!disable_version_select" class="mr-2" variant="outline-success" @click="saveOrder()">Save</b-button>
                <b-button :disabled="!disable_version_select" variant="outline-danger" @click="cancel()">Cancel</b-button>
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
    width: 60%;
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

export default {
  name: 'NewSalesOrder',
  components: {
    CertBadge,
    ChooseOrg,
    ChooseProduct,
    ChooseFormula,
    ChooseVariant
  },
  data: function () {
    return {
      clients: [],
      selected_client_buffer: null,
      selected_client: null,
      client_selected: false,
      products: [],
      selected_products: [],
      order_buffer: {
        order_date: new Date(),
        target_completion_date: new Date(new Date().setMonth(new Date().getMonth() + 3)),
        client_po: ''
      }
    }
  },
  computed: {
    loaded: function () {
      return this.clients.length > 0
    }
  },
  methods: {
    addVariant: function (index) {
      this.selected_products[index].selected_variants.push({
        qty: 0,
        percent_overage: 0,
        special_instructions: ''
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
    },
    removeRow: function (index) {
      this.selected_products.splice(index, 1)
    },
    addRow: function () {
      this.selected_products.push({
        product_id: null,
        product: null,
        selected_formula: null,
        variants: [],
        selected_variants: [],
        formulas: [],
        formula_id: null,
        formulation_version: null,
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
