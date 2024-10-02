<template>
  <div class="my_component">
    <div class="card my-2">
      <div class="card-body">
        <h2 class="card-title flex-grow-1">New Product Form</h2>

        <b-form>
          <div>
            <label><strong>Product Name</strong></label>
            <div class="d-flex justify-content-between" style="width:80%;">
              <b-form-input
                required
                v-model="product_name"
                placeholder="Product Name"
                aria-describedby="name-feedback"
                :class="['form-control', 'mb-2', 'mx-2', (product_name? '' : 'is-invalid')]"
                ></b-form-input>
              <div style="width:20%;" id="name-feedback" class="invalid-feedback">This is a required field.</div>
            </div>
          </div>

          <div>
            <label><strong>Client</strong></label>
            <div class="d-flex justify-content-between ml-2" style="width: 100%">
              <ChooseOrg @org="(o) => client = o" :organizations="organization_options" :selected="client.organization_id ? client : null" :org-req="true" :initial="false"></ChooseOrg>
            </div>
          </div>

          <div>
            <label><strong>Certifications</strong><br></label>
            <div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_usda_organic ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_usda_organic">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/usda_organic.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_made_with_organic ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_made_with_organic">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/made_with_organic.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_wildcrafted ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_wildcrafted">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/wildcrafted.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_fda ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_fda">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/fda_approved.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_gmp ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_gmp">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/good_manufacturing_practice.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_halal ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_halal">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/halal_certified.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_kosher ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_kosher">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/kosher_certified.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_gluten_free ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_gluten_free">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/gluten_free.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_national_sanitation_foundation ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_national_sanitation_foundation">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/nsf_international_logo.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_us_pharmacopeia ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_us_pharmacopeia">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/us_pharmacopeia.png')"></b-img>
                </label>
              </div>
              <div class="btn-group-toggle d-inline-block my-2 mr-4">
                <label :class="['btn', (certified_vegan ? 'btn-success' : 'btn-outline-success')]">
                  <input type="checkbox" v-model="certified_vegan">
                    <b-img circle style="width:9em;" :src="require('../../../assets/certifications/vegan.png')"></b-img>
                </label>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-end">
            <b-button variant="primary" @click="submit()">Submit</b-button>
          </div>
        </b-form>
      </div>
    </div>
  </div>
</template>

<style scoped>
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
import productDoc from './productDoc.js'
import { CustomRequest, genTempKey } from '../../../common/CustomRequest.js'
import ChooseOrg from '../../../components/ChooseOrg.vue'
// import vSelect from 'vue-select'

export default {
  name: 'NewProduct',
  components: {
    // vSelect,
    ChooseOrg
  },
  props: {
    orgId: {
      type: Number,
      default: 0
    },
    orgName: {
      type: String,
      default: null
    },
    orgInitial: {
      type: String,
      default: null
    }
  },
  data: function () {
    return {
      client: {
        organization_id: this.orgId,
        organization_primary_name: this.orgName,
        organization_primary_initial: this.orgInitial
      },
      organization_options: [],
      new_product_id: null,
      organization_id: this.orgId,
      product_name: null,
      certified_fda: false,
      certified_gmp: false,
      certified_made_with_organic: false,
      certified_wildcrafted: false,
      certified_usda_organic: false,
      certified_halal: false,
      certified_kosher: false,
      certified_gluten_free: false,
      certified_national_sanitation_foundation: false,
      certified_us_pharmacopeia: false,
      certified_non_gmo: false,
      certified_vegan: false,
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    submit: function () {
      if (!this.validateNewProduct()) {
        return false
      }

      const newProduct = {
        product_id: this.new_product_id,
        organization_id: this.client.organization_id,
        product_name: this.product_name,
        current_product: true,
        doc: productDoc,
        num_formula_versions: 0,
        num_manufacturing_versions: 0,
        certified_fda: this.certified_fda,
        certified_gmp: this.certified_gmp,
        certified_made_with_organic: this.certified_made_with_organic,
        certified_wildcrafted: this.certified_wildcrafted,
        certified_usda_organic: this.certified_usda_organic,
        certified_halal: this.certified_halal,
        certified_kosher: this.certified_kosher,
        certified_gluten_free: this.certified_gluten_free,
        certified_national_sanitation_foundation: this.certified_national_sanitation_foundation,
        certified_us_pharmacopeia: this.certified_us_pharmacopeia,
        certified_non_gmo: this.certified_non_gmo,
        certified_vegan: this.certified_vegan,
        timestamp_fetched: new Date().toISOString()
      }

      this.req.upsertRecord('Product_Master', newProduct)

      this.req.upsertRecord('Item_id', {
        item_id: genTempKey(),
        product_id: this.new_product_id,
        timestamp_fetched: new Date().toISOString()
      })

      this.req.sendRequest(this.$root.getOrigin()).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status === 201) {
          Object.values(resp.data[0].temp_key_lookup).forEach(item => {
            if (item.table_name === 'Product_Master') {
              this.$router.push({ path: `/catalogue/products/${item.new_id}` })
            }
          })
        }
      })
    },
    validateNewProduct: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Product',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }
      const createToast = this.$root.createToast

      let flag = true

      if (!this.product_name) {
        errorToast.message = 'Product Name is Required.'
        createToast(errorToast)
        flag = false
      }

      if (!this.client.organization_id) {
        errorToast.message = 'Invalid Client.'
        createToast(errorToast)
        flag = false
      }

      return flag
    },
    get_organizations: function () {
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
            const orgs = Object.values(data.data)
            this.organization_options = orgs.sort((a, b) => (a?.organization_primary_name > b?.organization_primary_name ? 1 : -1))
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
    }
  },
  watch: {
    certified_usda_organic: function (val) {
      if (val === true) {
        this.certified_non_gmo = true
        this.certified_wildcrafted = false
        this.certified_made_with_organic = false
      } else {
        this.certified_non_gmo = false
      }
    },
    certified_made_with_organic: function (val) {
      if (val === true) {
        this.certified_non_gmo = false
        this.certified_wildcrafted = false
        this.certified_usda_organic = false
      }
    },
    certified_wildcrafted: function (val) {
      if (val === true) {
        this.certified_non_gmo = true
        this.certified_usda_organic = false
        this.certified_made_with_organic = false
      }
    }
  },
  created: function () {
    this.new_product_id = genTempKey()
    this.get_organizations()
  }
}
</script>
