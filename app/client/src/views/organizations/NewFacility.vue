<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-if="!loaded">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid class="p-0">
      <b-card class=" my-2" v-if="loaded">
        <b-card-body>
          <div class="card-title d-flex align-items-center flex-wrap">
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2" src="../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <div>
              <div class="card-title d-flex align-items-center">
                <h1>{{ facility.building_name ? facility.building_name : 'New Facility' }}</h1>
              </div>
              <router-link :to="'/organizations/'+orgId" target="_blank"><h4 class="card-subtitle text-muted mb-2">{{ orgName }} {{ orgInitial ? '(' + orgInitial + ')' : '' }}</h4></router-link>
            </div>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#GeneralInfo">General Info</b-nav-item>
            <b-nav-item href="#Shipping">Shipping</b-nav-item>
            <b-nav-item href="#Address">Address</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class="my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">
          <h3 id="GeneralInfo">General Info<b-button v-if="!edit" v-b-tooltip.hover title="Edit Facility" @click="toggleEdit()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <div>
            <b-row>
              <b-col style="max-width:23%;"><label for="building_name"><strong>Building Name:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="building_name"
                    type="text"
                    v-model="facility.building_name"
                    required
                    :disabled="!edit"
                    aria-describedby="building_name-live-feedback"
                    :class="['form-control', (facility.building_name ? '' : 'is-invalid')]"
                    @input="update()"
                    v-on:keyup.enter="focus('building_type')"
                  >
                  <div id="building_name-live-feedback" class="invalid-feedback">This required field.</div>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:23%;"><label for="building_type"><strong>Building Type:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <v-select
                    id="building_type"
                    v-model="facility.building_type"
                    label='label'
                    placeholder="Select Building Type..."
                    :reduce="option => option.value"
                    :options="[
                      { 'value': 'Head_Office', 'label': 'Head Office' },
                      { 'value': 'Office', 'label': 'Office' },
                      { 'value': 'Distribution_Warehouse', 'label': 'Distribution Warehouse' },
                      { 'value': 'Manufacturing_Facility', 'label': 'Manufacturing Facility' },
                      { 'value': 'Storefront', 'label': 'Storefront' }
                    ]"
                    :disabled="!edit"
                    @input="update()"
                    class="wide"
                    :clearable="false"
                    :filterable="false"
                  ></v-select>
                </div>
              </b-col>
            </b-row>
          </div>
          <hr>
          <h3 id="Shipping">Shipping<b-button v-if="!edit" v-b-tooltip.hover title="Edit Facility" @click="toggleEdit()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <div>
            <b-row>
              <b-col style="max-width:23%;"><label for="ship_time"><strong>Ship Time:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="email_address_primary"
                    type="number"
                    v-model="facility.ship_time"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('ship_time_units')"
                  >
                </div>
                <div class="input-group mb-2">
                  <v-select
                    id="ship_time_units"
                    v-model="facility.ship_time_units"
                    label='label'
                    placeholder="Select Shipping Units..."
                    :reduce="option => option.value"
                    :options="[
                      { 'value': 'Days', 'label': 'Days' },
                      { 'value': 'Months', 'label': 'Months' }
                    ]"
                    :disabled="!edit"
                    @input="update()"
                    class="wide"
                  ></v-select>
                </div>
              </b-col>
            </b-row>
          </div>
          <hr>
          <h3 id="Address">Address<b-button v-if="!edit" v-b-tooltip.hover title="Edit Facility" @click="toggleEdit()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <div>
            <!-- <b-row v-if="person.organization_id === 1" class="mb-3">
              <b-col style="max-width:23%;"><label for="email_address_primary"><strong>PLX Employee:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <div v-if="!edit">
                    <span v-show="person.is_employee" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                    <span v-show="!person.is_employee" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
                  </div>
                  <div v-else>
                    <b-button @click="update()" v-show="person.is_employee" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                    <b-button @click="update()" v-show="!person.is_employee" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                  </div>
                </div>
              </b-col>
            </b-row> -->
            <b-row>
              <b-col style="max-width:14%;"><label for="street_1"><strong>Street 1:</strong></label></b-col>
              <b-col>
                <div class="mb-2">
                  <div class="d-flex">
                    <input
                      id="street_1_number"
                      type="number"
                      class="form-control mb-2 mr-2"
                      placeholder="Street Number"
                      :disabled="!edit"
                      v-model="facility.street_1_number"
                      @input="update()"
                    >
                    <v-select
                      id="street_1_direction"
                      v-model="facility.street_1_direction"
                      placeholder="Select Street Direction..."
                      :options="[ 'N', 'E', 'S', 'W' ]"
                      :disabled="!edit"
                      @input="update()"
                      :clearable="false"
                      :filterable="false"
                      class="mb-2 mr-2"
                      style="width: 20rem;"
                    ></v-select>
                    <input
                      id="street_1_number_suffix"
                      type="text"
                      class="form-control mb-2"
                      placeholder="Suffix"
                      :disabled="!edit"
                      v-model="facility.street_1_number_suffix"
                      @input="update()"
                    >
                  </div>
                  <div class="d-flex">
                    <input
                      id="street_1_name"
                      type="text"
                      class="form-control mb-2 mr-2"
                      placeholder="Street Name"
                      :disabled="!edit"
                      v-model="facility.street_1_name"
                      @input="update()"
                    >
                    <v-select
                      id="street_1_type"
                      v-model="facility.street_1_type"
                      placeholder="Select Street type..."
                      :options="[ 'Street', 'Lane', 'Avenue', 'Road', 'Way', 'Drive' ]"
                      :disabled="!edit"
                      @input="update()"
                      :clearable="false"
                      :filterable="false"
                      class="mb-2"
                      style="width: 20rem;"
                    ></v-select>
                  </div>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:14%;"><label for="street_2"><strong>Street 2:</strong></label></b-col>
              <b-col>
                <div class="mb-2">
                  <div class="d-flex">
                    <input
                      id="street_2_number"
                      type="number"
                      class="form-control mb-2 mr-2"
                      placeholder="Street Number"
                      :disabled="!edit"
                      v-model="facility.street_2_number"
                      @input="update()"
                    >
                    <v-select
                      id="street_2_direction"
                      v-model="facility.street_2_direction"
                      placeholder="Select Street Direction..."
                      :options="[ 'N', 'E', 'S', 'W' ]"
                      :disabled="!edit"
                      @input="update()"
                      :clearable="false"
                      :filterable="false"
                      class="mb-2 mr-2"
                      style="width: 20rem;"
                    ></v-select>
                    <input
                      id="street_2_number_suffix"
                      type="text"
                      class="form-control mb-2"
                      placeholder="Suffix"
                      :disabled="!edit"
                      v-model="facility.street_2_number_suffix"
                      @input="update()"
                    >
                  </div>
                  <div class="d-flex">
                    <input
                      id="street_2_name"
                      type="text"
                      class="form-control mb-2 mr-2"
                      placeholder="Street Name"
                      :disabled="!edit"
                      v-model="facility.street_2_name"
                      @input="update()"
                    >
                    <v-select
                      id="street_2_type"
                      v-model="facility.street_2_type"
                      placeholder="Select Street type..."
                      :options="[ 'Street', 'Lane', 'Avenue', 'Road', 'Way', 'Drive' ]"
                      :disabled="!edit"
                      @input="update()"
                      :clearable="false"
                      :filterable="false"
                      class="mb-2"
                      style="width: 20rem;"
                    ></v-select>
                  </div>
                </div>
              </b-col>
            </b-row>
            <b-row class="mb-2">
              <b-col style="max-width:14%;"><label for="city_town"><strong>City/Town:</strong></label></b-col>
              <b-col>
                <input
                    id="city_town"
                    type="text"
                    v-model="facility.city_town"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('local_municipality')"
                  >
              </b-col>
            </b-row>
            <b-row class="mb-2">
              <b-col style="max-width:14%;"><label for="local_municipality"><strong>Municipality:</strong></label></b-col>
              <b-col>
                <input
                    id="local_municipality"
                    type="text"
                    v-model="facility.local_municipality"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('governing_district')"
                  >
              </b-col>
            </b-row>
            <b-row class="mb-2">
              <b-col style="max-width:14%;"><label for="governing_district"><strong>State/Province:</strong></label></b-col>
              <b-col>
                <input
                    id="governing_district"
                    type="text"
                    v-model="facility.governing_district"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('country')"
                  >
              </b-col>
            </b-row>
            <b-row class="mb-2">
              <b-col style="max-width:14%;"><label for="country"><strong>Country:</strong></label></b-col>
              <b-col>
                <input
                    id="country"
                    type="text"
                    v-model="facility.country"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('city_town')"
                  >
              </b-col>
            </b-row>
          </div>
          <div v-show="edit">
            <b-button class="mr-2" variant="outline-success" @click="submit()">Save</b-button>
            <b-button variant="outline-danger" @click="cancel()">Cancel</b-button>
          </div>
        </b-card-body>
      </b-card>
    </b-container>

  </div>
</template>

<script>
import { CustomRequest, genTempKey } from '../../common/CustomRequest.js'
import vSelect from 'vue-select'
import { cloneDeep } from 'lodash'

export default {
  name: 'NewFacility',
  components: {
    vSelect
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
      id: this.$route.params.id,
      loaded: true,
      edit: true,
      new_id: null,
      original_facility: {},
      facility: {},
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    toggleEdit: function () {
      if (!this.edit) {
        this.original_facility = cloneDeep(this.facility)
      }
      this.edit = !this.edit
    },
    update: function () {
      const facility = {
        facility_id: this.new_id,
        organization_id: this.orgId,
        building_name: this.facility.building_name,
        building_type: this.facility.building_type,
        notes: this.facility.notes,
        ship_time: this.facility.ship_time,
        ship_time_in_days: this.facility.ship_time_in_days,
        ship_time_units: this.facility.ship_time_units,
        street_1_direction: this.facility.street_1_direction,
        street_1_name: this.facility.street_1_name,
        street_1_number: this.facility.street_1_number,
        street_1_number_suffix: this.facility.street_1_number_suffix,
        street_1_type: this.facility.street_1_type,
        street_2_direction: this.facility.street_2_direction,
        street_2_name: this.facility.street_2_name,
        street_2_number: this.facility.street_2_number,
        street_2_number_suffix: this.facility.street_2_number_suffix,
        street_2_type: this.facility.street_2_type,
        local_municipality: this.facility.local_municipality,
        city_town: this.facility.city_town,
        governing_district: this.facility.governing_district,
        country: this.facility.country,
        postal_area: this.facility.postal_area,
        address_type: this.facility.address_type,
        address_type_identifier: this.facility.address_type_identifier,
        timestamp_fetched: this.facility.timestamp_fetched
      }
      this.req.updateUpsertRecord('Facilities', 'facility_id', this.new_id, facility)
    },
    validate: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Facility',
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

      if (!this.facility.building_name) {
        errorToast.message = 'Facility must have a building name.'
        createToast(errorToast)
        valid = false
      }

      if (this.facility.building_type === null) {
        errorToast.message = 'Facility must have a building type.'
        createToast(errorToast)
        valid = false
      }

      const validBuildingTypes = ['Head_Office', 'Office', 'Distribution_Warehouse', 'Manufacturing_Facility', 'Storefront']
      if (!validBuildingTypes.includes(this.facility.building_type)) {
        errorToast.message = 'Facility building type is invalid.'
        createToast(errorToast)
        valid = false
      }

      return valid
    },
    submit: async function () {
      // Check valid formula
      this.loaded = false
      if (!this.validate()) {
        this.loaded = true
        return
      }

      const resp = await this.req.sendRequest(this.$root.getOrigin())

      const createToast = this.$root.createToast
      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status === 201) {
        Object.values(resp.data[0].temp_key_lookup).forEach(item => {
          if (item.table_name === 'Facilities') {
            this.$router.push({ path: `/organizations/facilities/${item.new_id}` })
          }
        })
      } else {
        this.edit = false
        this.loaded = true
      }
    },
    cancel: function () {
      this.facility = cloneDeep(this.original_facility)
      this.edit = false
      this.$router.push({ path: `/organizations/${this.orgId}` })
    },
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    getFacility: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/organizations/facilities?facility_id=' + this.id + '&populate=organizations'
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
            this.facility = data.data[0]
            // eslint-disable-next-line
            console.log(this.facility)
            this.loaded = true
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
    this.new_id = genTempKey()
    this.facility.timestamp_fetched = new Date().toISOString()
    this.update()
  }
}
</script>

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
.wide {
  width: 100%;
}
</style>
