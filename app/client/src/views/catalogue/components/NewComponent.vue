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
        <h2 class="card-title flex-grow-1">New Component Form</h2>

        <b-form>
          <div class="d-flex justify-content-between">
            <p><strong>Aliases</strong></p>
              <b-button variant="outline-info" class="m-2" v-on:click="addName()">New Name</b-button>
          </div>
          <div v-for="name in edit_names_buffer" :key="'edit' + name.name_id">
            <div class="mb-2 d-flex justify-content-start">
              <label class="sr-only" for="inline-form-input-name">name</label>
              <div class="d-flex justify-content-between" style="width:50%;">
                <b-form-input
                  required
                  v-model="name.component_name"
                  placeholder="Component Name"
                  aria-describedby="name-feedback"
                  :class="['form-control', 'mb-2', 'mx-2', (!!name.component_name ? '' : 'is-invalid')]"
                  ></b-form-input>
                <div style="width:40%;" id="name-feedback" class="invalid-feedback">This is a required field.</div>
              </div>
              <div class="btn-group-toggle d-inline-block mb-2 mx-2 d-flex justify-content-center">
                <label :class="['btn', name.primary_name ? 'btn-primary' : 'btn-outline-primary', name.primary_name ? 'disabled' : '']">
                  <input v-on:click="radioNames(name.name_id, 'primary')" type="checkbox" name="Primary Name" :disabled="name.primary_name" v-model="name.primary_name">Primary Name
                </label>
              </div>
              <div v-show="'botanical_name' in name" class="btn-group-toggle d-inline-block mb-2 mx-2 d-flex justify-content-center">
                <label :class="['btn', name.botanical_name ? 'btn-success' : 'btn-outline-success']">
                  <input v-on:click="radioNames(name.name_id, 'botanical')" type="checkbox" name="Botanical Name" v-model="name.botanical_name">Botanical Name
                </label>
              </div>
              <div class="mb-2 mx-2">
                <b-button variant="outline-danger" v-show="!name.primary_name" v-on:click="deleteName(name.name_id)">Delete</b-button>
              </div>
            </div>
          </div>

          <b-form-group>
            <label><strong>Component Type</strong><br></label>
            <v-select
              required
              v-model="component_type"
              :options="component_options"
              label="text"
              :reduce="type => type.value"
              placeholder="Select Component Type"
              aria-describedby="component-type-feedback"
              :class="[(!!component_type ? '' : 'is-invalid')]"
            ></v-select>
            <div id="component-type-feedback" class="invalid-feedback">This is a required field.</div>
          </b-form-group>

          <b-form-group>
            <label><strong>Stock Keeping Measure Unit</strong><br></label>
            <v-select
              required
              :disabled="component_type === 'powder' || component_type === 'liquid' || component_type === 'capsule'"
              v-model="unit_type"
              :options="unit_options"
              label="text"
              :reduce="unit => unit.value"
              placeholder="Select Stock Keeping Measure Unit"
              aria-describedby="unit-type-feedback"
              :class="[(!!unit_type ? '' : 'is-invalid')]"
            ></v-select>
            <div id="unit-type-feedback" class="invalid-feedback">This is a required field.</div>
          </b-form-group>

          <div v-show="component_type === 'powder' || component_type === 'liquid' || component_type === 'capsule'">
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

          <div>
            <label><strong>Component Brand</strong></label>
            <div class="d-flex justify-content-between ml-2" style="width: 100%" id="brand_select">
              <div class="custom-control custom-checkbox">
                <input :disabled="brand_not_allowed" class="custom-control-input" id="brand_association" type="checkbox" v-model="no_brand" name="brand_association">
                <label class="custom-control-label" for="brand_association">
                  Brand Association
                </label>
              </div>
              <ChooseOrg :disabled-prop="!no_brand || brand_not_allowed" @org="(o) => brand = o" :organizations="organization_options" :selected="brand.organization_id ? brand : null" :initial="false"></ChooseOrg>
            </div>
            <b-tooltip v-if="brand_not_allowed" target="brand_select" triggers="hover">Brand associations are not allowed for ingredients.</b-tooltip>
          </div>

          <div class="d-flex justify-content-end">
            <b-button variant="primary" @click="submit()">Submit</b-button>
          </div>
        </b-form>
      </div>
    </div>
    <div style="display:none;">
      <NamesComponent></NamesComponent>
      <CertBadge></CertBadge>
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
import ingredientDoc from './ingredientDocTemp.js'
import compDoc from './compDocTemp.js'
import { CustomRequest, genTempKey } from '../../../common/CustomRequest.js'
import ChooseOrg from '../../../components/ChooseOrg.vue'
import vSelect from 'vue-select'
import NamesComponent from './NamesComponent.vue'
import CertBadge from '../../../components/CertBadge.vue'

export default {
  name: 'NewComponent',
  components: {
    vSelect,
    ChooseOrg,
    NamesComponent,
    CertBadge
  },
  props: {
    orgId: {
      type: Number,
      default: null
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
      loaded: true,
      brand: {
        organization_id: this.orgId,
        organization_primary_name: this.orgName,
        organization_primary_initial: this.orgInitial
      },
      no_brand: !!this.orgId,
      organization_options: [],
      edit_names_buffer: [],
      new_component_id: null,
      component_type: null,
      // Label related items are only created via Products Page
      component_options: [
        { value: 'powder', text: 'Powder' },
        { value: 'liquid', text: 'Liquid' },
        { value: 'container', text: 'Container' },
        // { value: 'pouch', text: 'Pouch' },
        { value: 'shrink_band', text: 'Shrink Band' },
        { value: 'lid', text: 'Lid' },
        // { value: 'label', text: 'Label' },
        { value: 'capsule', text: 'Capsule' },
        { value: 'misc', text: 'Miscellaneous' },
        { value: 'scoop', text: 'Scoop' },
        { value: 'desiccant', text: 'Desiccant' },
        { value: 'box', text: 'Box' },
        // { value: 'carton', text: 'Carton' },
        { value: 'packaging_material', text: 'Packaging Material' }
      ],
      unit_type: null,
      unit_options: [
        { value: 'grams', text: 'Grams (g)' },
        { value: 'kilograms', text: 'Kilograms (kg)' },
        { value: 'pounds', text: 'Pounds (lbs)' },
        { value: 'liters', text: 'Liters (l)' },
        { value: 'units', text: 'Units' },
        { value: 'boxes', text: 'Boxes' },
        { value: 'pallets', text: 'Pallets' },
        { value: 'rolls', text: 'Rolls' },
        { value: 'totes', text: 'Totes' },
        { value: 'barrels', text: 'Barrels' }
      ],
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
      req: new CustomRequest(this.$cookies.get('session')),
      flash_errors: [],
      duplicate_flag: null
    }
  },
  methods: {
    buildDuplicateModalMessage: function (testName, score, potentialDuplicate) {
      console.log('potentialDuplicate:', potentialDuplicate)
      const h = this.$createElement
      const messageVNode = h('div', [
        h('p', [
          `'${testName}' (new component) has a ${score}% match with '${potentialDuplicate.component_name}' (pre-existing component).  Are these two components the same?`
        ]),
        h('p', [
          `If so, click YES to go to the '${potentialDuplicate.component_name}' spec page.`
        ]),
        h('p', [
          'If not, click NO to continue creating the new component.'
        ]),
        potentialDuplicate.component_names.length > 0 ? h('p', ['The following names and/or certifications are associated with the existing component:']) : null,
        h('div', [
          potentialDuplicate.component_names.length > 0 ? h(NamesComponent, { props: { pNames: potentialDuplicate.component_names, namingType: 'component', allowEdit: false, id: potentialDuplicate.component_id, hideHeader: true } }) : null
        ]),
        h('div', [
          h(CertBadge, { props: { data: potentialDuplicate } })
        ])
      ])
      return messageVNode
    },
    handleDuplicates: async function (data) {
      this.duplicate_flag = false
      for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < data[i].similar_names.length; j++) {
          const potentialDuplicate = data[i].similar_names[j]
          const testName = data[i].component_name
          const score = data[i].similar_names[j].duplicate_probability_score_name
          const modal = {
            title: `Please Confirm '${testName}' is not a Duplicate`,
            size: 'lg',
            buttonSize: 'md',
            okVariant: 'danger',
            okTitle: 'YES',
            cancelTitle: 'NO',
            cancelVariant: 'success',
            footerClass: 'p-2',
            hideHeaderClose: true,
            centered: true,
            hideBackdrop: false,
            noStacking: true,
            noCloseOnBackdrop: true
          }
          const value = await this.$bvModal.msgBoxConfirm(
            [this.buildDuplicateModalMessage(testName, score, potentialDuplicate)], modal
          )
          if (this.duplicate_flag) {
            return false
          }
          if (value) {
            this.duplicate_flag = true
            this.$router.push({ path: `/catalogue/components/${potentialDuplicate.component_id}` })
            return false
          }
        }
      }
      return true
    },
    checkComponentAlreadyExists: async function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/submit/check_component'
      // eslint-disable-next-line
      console.log(
        'POST ' + fetchRequest
      )
      return fetch(fetchRequest, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(this.edit_names_buffer)
      }).then(response => {
        return response.json().then(jsonData => {
          if (response.status === 200) {
            return jsonData.data
          } else if (response.status === 401) {
            this.form_messages = jsonData.messages.form
            return false
          } else {
            this.flash_messages = jsonData.messages.flash
            const createToast = this.$root.createToast
            this.flash_messages.forEach(function (message) {
              createToast(message)
            })
            return false
          }
        })
      }).catch(error => {
        // eslint-disable-next-line
        console.log(error)
        this.flash_errors.push(error)
        // eslint-disable-next-line
        console.log(this.flash_errors)
        return false
      })
    },
    submit: async function () {
      this.loaded = false
      if (!this.validateNewComponent()) {
        this.loaded = true
        return false
      }

      const result1 = await this.checkComponentAlreadyExists()
      if (!result1) {
        return false
      }
      const result2 = await this.handleDuplicates(result1)
      if (!result2) {
        return false
      }

      this.req.upsertRecord('Item_id', { item_id: genTempKey(), component_id: this.new_component_id, timestamp_fetched: new Date().toISOString() })

      const newComponent = {
        component_id: this.new_component_id,
        component_type: this.component_type,
        brand_id: (this.no_brand || this.brand_not_allowed) ? null : this.brand.organization_id,
        units: this.unit_type,
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
        doc: {},
        timestamp_fetched: new Date().toISOString()
      }

      if (this.component_type === 'powder' || this.component_type === 'liquid' || this.component_type === 'capsule') {
        newComponent.doc = ingredientDoc
      } else {
        newComponent.doc = compDoc
      }

      let primaryNameTempKey = ''

      this.req.upsertRecord('Components', newComponent)
      this.edit_names_buffer.forEach(name => {
        this.req.upsertRecord('Component_Names', name)
        if (name.primary_name) {
          primaryNameTempKey = name.name_id
        }
      })

      const createToast = this.$root.createToast

      const resp1 = await this.req.sendRequest(this.$root.getOrigin())

      if (resp1.status !== 201) {
        resp1.messages.flash.forEach(message => {
          createToast(message)
        })
        this.loaded = true
        return false
      }

      const tempKeyLookup = this.req.getTempKeyLookup()
      this.req = new CustomRequest(this.$cookies.get('session'))

      const updateComponent = {
        component_id: tempKeyLookup[this.new_component_id].new_id,
        primary_name_id: tempKeyLookup[primaryNameTempKey].new_id,
        timestamp_fetched: new Date().toISOString()
      }
      this.req.upsertRecord('Components', updateComponent)
      const resp2 = await this.req.sendRequest(this.$root.getOrigin())

      resp2.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp2.status !== 201) {
        this.loaded = true
        return false
      }

      this.$router.push({ path: `/catalogue/components/${updateComponent.component_id}` })
      return true
    },
    validateNewComponent: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Component',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }
      const createToast = this.$root.createToast

      let flag = true

      if (this.component_type === null) {
        errorToast.message = 'Component Type is required.'
        createToast(errorToast)
        flag = false
      }

      if (this.unit_type === null) {
        errorToast.message = 'Stock Keeping Measure Unit is required.'
        createToast(errorToast)
        flag = false
      }

      if (this.edit_names_buffer.length === 0) {
        errorToast.message = 'At least one name is required.'
        createToast(errorToast)
        flag = false
      }

      let primaryNameCount = 0

      this.edit_names_buffer.forEach(name => {
        if (name.component_name === '') {
          errorToast.message = 'Name cannot be empty.'
          createToast(errorToast)
          flag = false
        }

        if (name.primary_name) {
          primaryNameCount += 1
        }
      })

      if (primaryNameCount !== 1) {
        errorToast.message = 'A Primary Name is required.'
        createToast(errorToast)
        flag = false
      }

      return flag
    },
    radioNames: function (id, flag) {
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].name_id === id) {
          if (flag === 'botanical') {
            this.edit_names_buffer[i].botanical_name = true
          } else if (flag === 'primary') {
            this.edit_names_buffer[i].primary_name = true
          } else {
            continue
          }
        } else {
          if (flag === 'botanical') {
            this.edit_names_buffer[i].botanical_name = false
          } else if (flag === 'primary') {
            this.edit_names_buffer[i].primary_name = false
          } else {
            continue
          }
        }
      }
    },
    addName: function () {
      const newName = this.createName()
      this.edit_names_buffer.push(newName)
    },
    deleteName: function (id) {
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].name_id === id) {
          this.edit_names_buffer.splice(i, 1)
        }
      }
    },
    createName: function () {
      const newName = {
        name_id: genTempKey(),
        component_id: this.new_component_id,
        component_name: '',
        primary_name: false,
        botanical_name: false,
        timestamp_fetched: new Date().toISOString()
      }
      return newName
    },
    load_doc: function (val) {
      if (val === 'powder' || val === 'liquid' || val === 'capsule') {
        this.doc = ingredientDoc
      } else {
        this.doc = compDoc
      }
    },
    get_organizations: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/organizations?org-type=supplier'
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
    component_type: function (val) {
      if (val === 'powder') {
        this.unit_type = 'kilograms'
        this.brand.organization_id = 0
        this.brand.organization_primary_name = null
        this.brand.organization_primary_initial = null
        this.no_brand = false
      } else if (val === 'liquid') {
        this.unit_type = 'liters'
        this.brand.organization_id = 0
        this.brand.organization_primary_name = null
        this.brand.organization_primary_initial = null
        this.no_brand = false
      } else {
        this.unit_type = ''
        this.certified_fda = false
        this.certified_gmp = false
        this.certified_made_with_organic = false
        this.certified_wildcrafted = false
        this.certified_usda_organic = false
        this.certified_halal = false
        this.certified_kosher = false
        this.certified_gluten_free = false
        this.certified_national_sanitation_foundation = false
        this.certified_us_pharmacopeia = false
        this.certified_non_gmo = false
        this.certified_vegan = false
      }
      this.load_doc(val)
    },
    certified_usda_organic: function (val) {
      if (val === true) {
        this.certified_non_gmo = true
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
    }
  },
  computed: {
    brand_not_allowed: function () {
      if (this.component_type === 'powder' ||
          this.component_type === 'liquid' ||
          this.component_type === 'capsule' ||
          this.component_type === null) {
        return true
      } else {
        return false
      }
    }

  },
  created: function () {
    this.new_component_id = genTempKey()
    const newName = this.createName()
    // newName.primary_name = true
    this.edit_names_buffer.push(newName)
    this.radioNames(this.edit_names_buffer[0].name_id, 'primary')
    this.get_organizations()
  }
}
</script>
