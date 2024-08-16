<template>
  <div class="my_component d-flex flex-wrap justify-content-center">
    <div class="card my-2" v-if="!loaded" style="box-shadow: 0 20px 40px rgba(0,0,0,.2);">
      <div class="card-body">
        <div class="d-flex justify-content-center">
          <div class="spinner-border text-primary" role="status"></div>
        </div>
      </div>
    </div>

    <b-container fluid class="p-0">
      <b-card class=" my-2" v-if="loaded" style="box-shadow: 0 20px 40px rgba(0,0,0,.2);">
        <b-card-body>
          <div class="card-title d-flex align-items-center flex-wrap">
            <b-img style="max-width: 15rem;" class="d-none d-print-inline p-2" src="../../assets/Company Images/logos jpg/Cropped Logo.jpg"></b-img>
            <h2 class="card-title">{{ org_data.organization_primary_name }} {{ '(' + org_data.organization_primary_initial + ')' }}
              <b-badge v-show="org_data.supplier" variant="light" class="mr-2 border">Supplier</b-badge>
              <b-badge v-show="org_data.client" variant="light" class="mr-2 border">Client</b-badge>
              <b-badge v-show="org_data.lab" variant="light" class="mr-2 border">Lab</b-badge>
              <b-badge v-show="org_data.courier" variant="light" class="mr-2 border">Courier</b-badge>
              <b-badge v-show="org_data.other" variant="light" class="mr-2 border">Other</b-badge>
              <b-badge v-show="org_data.risk_level === 'UNKNOWN'" variant="danger" class="mr-2 border">Unknown Risk</b-badge>
              <b-badge v-show="org_data.risk_level === 'Low_Risk' || org_data.risk_level === 'No_Risk'" variant="success" class="mr-2 border">Low Risk</b-badge>
              <b-badge v-show="org_data.risk_level === 'Medium_Risk'" variant="warning" class="mr-2 border">Medium Risk</b-badge>
              <b-badge v-show="org_data.risk_level === 'High_Risk'" variant="danger" class="mr-2 border">High Risk</b-badge>
            </h2>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#GeneralInfo" @click="scrollIntoView" :disabled="!activeSection('org_data')">General Info</b-nav-item>
            <b-nav-item href="#Aliases" @click="scrollIntoView" :disabled="!activeSection('names')">Aliases</b-nav-item>
            <b-nav-item href="#SupplierRiskAssessments" @click="scrollIntoView" :disabled="!activeSection('supplier_risk_assessment')">Supplier Risk Assessments</b-nav-item>
            <b-nav-item href="#People" @click="scrollIntoView" :disabled="!activeSection('people')">People</b-nav-item>
            <b-nav-item href="#Facilities" @click="scrollIntoView" :disabled="!activeSection('facilities')">Facilities</b-nav-item>
            <b-nav-item href="#Products" @click="scrollIntoView" :disabled="!activeSection('products')" v-show="org_data.client">Products</b-nav-item>
            <b-nav-item href="#Components" @click="scrollIntoView" :disabled="!activeSection('components')" v-show="org_data.supplier">Components</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">

          <!-- General Info -->
          <div v-show="activeSection('org_data')">
            <h3 id="GeneralInfo">General Info<b-button v-show="!edit_org" v-b-tooltip.hover :title="'Edit General Organization Informaion.'" v-on:click="setOrgBuffer()" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>

            <div class="d-flex mb-3">
              <strong class='mr-3'>Organization Type(s): </strong>
              <div v-if="edit_org">
                <b-form-group aria-describedby="organization-type-live-feedback" :class="[ ( edit_org_buffer.supplier || edit_org_buffer.client || edit_org_buffer.lab || edit_org_buffer.courier || edit_org_buffer.other ? '' : 'is-invalid')]">
                  <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
                    <input class="custom-control-input" type="checkbox" name="supplier" id="supplier" v-model="edit_org_buffer.supplier">
                    <label class="custom-control-label" for="supplier">Supplier</label>
                  </div>
                  <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
                    <input class="custom-control-input" type="checkbox" name="client" id="client" v-model="edit_org_buffer.client">
                    <label class="custom-control-label" for="client">Client</label>
                  </div>
                  <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
                    <input class="custom-control-input" type="checkbox" name="lab" id="lab" v-model="edit_org_buffer.lab">
                    <label class="custom-control-label" for="lab">Laboratory</label>
                  </div>
                  <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
                    <input class="custom-control-input" type="checkbox" name="courier" id="courier" v-model="edit_org_buffer.courier">
                    <label class="custom-control-label" for="courier">Courier</label>
                  </div>
                  <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
                    <input class="custom-control-input" type="checkbox" name="other" id="other" v-model="edit_org_buffer.other">
                    <label class="custom-control-label" for="other">Other</label>
                  </div>
                </b-form-group>
                <div id="organization-type-live-feedback" class="invalid-feedback">At least one organization type must be selected.</div>
              </div>
              <h3 v-else>
                <b-badge v-show="org_data.supplier" variant="light" class="mr-2 border">Supplier</b-badge>
                <b-badge v-show="org_data.client" variant="light" class="mr-2 border">Client</b-badge>
                <b-badge v-show="org_data.lab" variant="light" class="mr-2 border">Lab</b-badge>
                <b-badge v-show="org_data.courier" variant="light" class="mr-2 border">Courier</b-badge>
                <b-badge v-show="org_data.other" variant="light" class="mr-2 border">Other</b-badge>
              </h3>
            </div>

            <div class="mb-3">
              <strong class='mr-3'>Notes: </strong>
              <b-form-group>
                <b-form-textarea
                  :disabled="!edit_org"
                  id="textarea"
                  v-model="edit_org_buffer.notes"
                  placeholder="Enter notes here..."
                  rows="3"
                  max-rows="6"
                ></b-form-textarea>
              </b-form-group>
            </div>

            <div class="mb-3">
              <strong class='mr-3'>Website: </strong>
              <b-form-group v-show="edit_org">
                <b-form-input
                  :disabled="!edit_org"
                  id="website_url"
                  v-model="edit_org_buffer.website_url"
                  placeholder="Enter website URL"
                  type="url"
                ></b-form-input>
              </b-form-group>
              <p v-show="!edit_org" class="text-info">
                <b-link :exact="true" :exact-path="true" :href="buildURL(org_data.website_url)" target="_blank">{{ org_data.website_url }}</b-link>
              </p>
            </div>

            <div class="d-flex">
              <div v-show="edit_org">
                <b-button variant="outline-danger" class="m-2" v-on:click="cancel()">Cancel</b-button>
                <b-button type="submit" variant="outline-success" class="m-2" v-on:click="submit()">Save</b-button>
              </div>
            </div>
          </div>
          <hr v-show="activeSection('org_data')">

          <!-- Alias Names -->
          <NamesComponent
            v-show="activeSection('names')"
            :p-names="org_data.organization_names"
            :id="org_data.organization_id"
            naming-type="organization"
            :allow-edit="true"
            v-on:edit-names="(e) => edit_names = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="refreshParent"
          ></NamesComponent>
          <hr v-show="activeSection('names')">

          <!-- Risk Assessments -->
          <SupplierRiskAssessments
            v-if="org_data.supplier"
            v-show="activeSection('supplier_risk_assessment')"
            :id="org_data.organization_id"
            :doc="org_data.doc"
            :org-name="org_data.organization_primary_name"
            v-on:edit-risk-assessment="(e) => edit_supplier_risk_assessment = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="refreshParent"
          ></SupplierRiskAssessments>
          <hr v-show="activeSection('supplier_risk_assessment')">

          <!-- People -->
          <div v-show="activeSection('people')">
            <h3 id="People">People<b-button @click="$router.push({ path:'/organizations/people/create', query: { orgId: org_data.organization_id, orgName: org_data.organization_primary_name, orgInitial: org_data.organization_primary_initial } })" v-b-tooltip.hover :title="'Add a new product.'" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="plus" class="d-print-none"></b-icon></b-button></h3>
            <b-table striped :items="sorted_people" show-empty id="people-table" :per-page="perPage" :current-page="currentProductPage" bordered
              :fields="[
                { key: 'name', label: 'Name', thStyle: { width: '25%' } },
                { key: 'job_description', label: 'Title', thStyle: { width: '10%' } },
                { key: 'email_address_primary', label: 'Email' },
                { key: 'phone_number_primary', label: 'Phone' }
              ]">
              <template #cell(name)="data">
                <b-button v-on:click.stop class="mr-2" variant="light" :to="'/organizations/people/'+data.item.person_id " target="_blank"><b-icon icon="box"></b-icon></b-button>
                <b class="text-info">{{ data.item.first_name + ' ' + data.item.last_name }}</b>
              </template>
              <template #cell(job_description)="data">
                <h4 v-if="data.item.termination_date"><b-badge variant='danger'>Terminated</b-badge></h4>
                <h4 v-else><b-badge variant='light'>{{ data.item.job_description }}</b-badge></h4>
              </template>
              <template #cell(email_address_primary)="data">
                <b-link :href="'mailto:'+data.item.email_address_primary" target="_blank">{{ data.item.email_address_primary }}</b-link>
              </template>
              <template #cell(phone_number_primary)="data">
                <b-link :href="'tel:'+data.item.phone_number_primary">{{ formatPhoneNumber(data.item.phone_number_primary) }}</b-link>
              </template>
              <template #empty="scope">
                <div class="d-flex justify-content-center">
                  <h5>{{ scope.emptyText }}</h5>
                </div>
              </template>
            </b-table>
            <div class="d-flex justify-content-center">
              <b-pagination
                v-model="currentProductPage"
                :total-rows="org_data.people.length"
                :per-page="perPage"
                aria-controls="people-table"
              ></b-pagination>
            </div>
          </div>
          <hr v-show="activeSection('people')">

          <!-- Facilities -->
          <div v-show="activeSection('facilities')">
            <h3 id="Facilities">Facilities<b-button @click="$router.push({ path:'/organizations/facilities/create', query: { orgId: org_data.organization_id, orgName: org_data.organization_primary_name, orgInitial: org_data.organization_primary_initial } })" v-b-tooltip.hover :title="'Add a new product.'" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="plus" class="d-print-none"></b-icon></b-button></h3>
            <b-table striped :items="org_data.facilities" show-empty id="facilities-table" :per-page="perPage" :current-page="currentProductPage" bordered
              :fields="[
                { key: 'building_name', label: 'Building', thStyle: { width: '25%' } },
                { key: 'building_type', label: 'Type' },
                { key: 'country', label: 'Country' },
                { key: 'governing_district', label: 'State/Province' },
                { key: 'city_town', label: 'City' },
                { key: 'postal_area', label: 'Postal Code' },
                { key: 'location', label: 'Location', thStyle: { width: '8%' } },
                { key: 'ship_time', label: 'Ave Ship Time' }
              ]">
              <template #cell(building_name)="data">
                <b-button v-on:click.stop class="mr-2" variant="light" :to="'/organizations/facilities/'+data.item.facility_id " target="_blank"><b-icon icon="box"></b-icon></b-button>
                <b class="text-info">{{ data.value }}</b>
              </template>
              <template #cell(building_type)="data">
                <h4><b-badge variant='light'>{{ data.item.building_type.replace('_', ' ') }}</b-badge></h4>
              </template>
              <template #cell(country)="data">
                <h4><b-badge variant='light'>{{ data.item.country }}</b-badge></h4>
              </template>
              <template #cell(governing_district)="data">
                <h4><b-badge variant='light'>{{ data.item.governing_district }}</b-badge></h4>
              </template>
              <template #cell(city_town)="data">
                <h4><b-badge variant='light'>{{ data.item.city_town }}</b-badge></h4>
              </template>
              <template #cell(postal_area)="data">
                <h4><b-badge variant='light'>{{ data.item.postal_area }}</b-badge></h4>
              </template>
              <template #cell(location)="data">
                <div class="d-flex justify-content-center">
                  <b-button variant='light' :href="'https://www.google.com/maps/search/?api=1&query='+formatLocationURLQuery(data.item)" target="_blank"><b-icon icon="pin-map"></b-icon></b-button>
                </div>
              </template>
              <template #cell(ship_time)="data">
                <h4><b-badge variant='light'>{{ data.item.ship_time }} {{ data.item.ship_time_units }}</b-badge></h4>
              </template>
              <template #empty="scope">
                <div class="d-flex justify-content-center">
                  <h5>{{ scope.emptyText }}</h5>
                </div>
              </template>
            </b-table>
            <div class="d-flex justify-content-center">
              <b-pagination
                v-model="currentProductPage"
                :total-rows="org_data.facilities.length"
                :per-page="perPage"
                aria-controls="facilities-table"
              ></b-pagination>
            </div>
          </div>
          <hr v-show="activeSection('facilities')">

          <!-- Products -->
          <div v-show="activeSection('products')">
            <h3 id="Products">Products<b-button @click="$router.push({ path:'/catalogue/products/create', query: { orgId: org_data.organization_id, orgName: org_data.organization_primary_name, orgInitial: org_data.organization_primary_initial } })" v-b-tooltip.hover :title="'Add a new product.'" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="plus" class="d-print-none"></b-icon></b-button></h3>
            <b-table striped :items="org_data.products" show-empty id="products-table" :per-page="perPage" :current-page="currentProductPage" bordered
              :fields="[
                { key: 'product_name', label: 'Product', thStyle: { width: '40%' } },
                { key: 'certs', label: 'Certs' }
              ]">
              <template #cell(product_name)="data">
                <b-button v-on:click.stop class="mr-2" variant="light" :to="'/catalogue/products/'+data.item.product_id " target="_blank"><b-icon icon="box"></b-icon></b-button>
                <b class="text-info">{{ data.value }}</b>
              </template>
              <template #cell(certs)="data">
                <CertBadge :data="data.item"></CertBadge>
              </template>
              <template #empty="scope">
                <div class="d-flex justify-content-center">
                  <h5>{{ scope.emptyText }}</h5>
                </div>
              </template>
            </b-table>
            <div class="d-flex justify-content-center">
              <b-pagination
                v-model="currentProductPage"
                :total-rows="org_data.products.length"
                :per-page="perPage"
                aria-controls="products-table"
              ></b-pagination>
            </div>
          </div>
          <hr v-show="activeSection('products')">

          <!-- Components -->
          <div v-show="activeSection('components')">
            <h3 id="Components">Components<b-button @click="$router.push({ path:'/catalogue/components/create', query: { orgId: org_data.organization_id, orgName: org_data.organization_primary_name, orgInitial: org_data.organization_primary_initial } })" v-b-tooltip.hover :title="'Add a new component.'" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="plus" class="d-print-none"></b-icon></b-button></h3>
            <b-table striped :items="org_data.components" show-empty id="components-table" :per-page="perPage" :current-page="currentComponentPage" bordered
              :fields="[
                { key: 'component_primary_name', label: 'Component', thStyle: { width: '40%' } },
                { key: 'certs', label: 'Certs' }
              ]">
              <template #cell(component_primary_name)="data">
                <b-button v-on:click.stop class="mr-2" variant="light" :to="'/catalogue/components/'+data.item.component_id " target="_blank"><b-icon icon="box"></b-icon></b-button>
                <b class="text-info">{{ data.value }}</b>
              </template>
              <template #cell(certs)="data">
                <CertBadge :data="data.item"></CertBadge>
              </template>
              <template #empty="scope">
                <div class="d-flex justify-content-center">
                  <h5>{{ scope.emptyText }}</h5>
                </div>
              </template>
            </b-table>
            <div class="d-flex justify-content-center">
              <b-pagination
                v-model="currentComponentPage"
                :total-rows="org_data.components.length"
                :per-page="perPage"
                aria-controls="components-table"
              ></b-pagination>
            </div>
          </div>
          <hr>

        </b-card-body>
      </b-card>
    </b-container>

  </div>
</template>

<script>
import { CustomRequest } from '../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'
import NamesComponent from './NamesComponent.vue'
import CertBadge from '../../components/CertBadge.vue'
import SupplierRiskAssessments from './SupplierRiskAssessments.vue'

export default {
  name: 'OrganizationDetail',
  components: {
    NamesComponent,
    CertBadge,
    SupplierRiskAssessments
  },
  data: function () {
    return {
      perPage: 8,
      currentProductPage: 1,
      currentComponentPage: 1,
      id: this.$route.params.id,
      loaded: false,
      org_data: {},
      edit_names: false,
      edit_org: false,
      edit_supplier_risk_assessment: false,
      edit_org_buffer: {},
      sorted_people: [],
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    buildURL: function (url) {
      if (url && !url.startsWith('http')) {
        return 'http://' + url
      }
      return url
    },
    sortPeople: function (a, b) {
      if (a.termination_date && b.termination_date) {
        return a.termination_date > b.termination_date ? 1 : -1
      }
      if (a.termination_date) {
        return 1
      }
      if (b.termination_date) {
        return -1
      }
      return a.first_name > b.first_name ? 1 : -1
    },
    formatLocationURLQuery: function (facility) {
      // 696 undefined 696 undefined Hurricane Utah 84737 USA
      const street1 = facility.street_1_name ? facility.street_1_name : '' + facility.street_1_number ? facility.street_1_number?.toString() : '' + ' ' + facility.street_1_direction ? facility.street_1_direction : ''
      const street2 = facility.street_2_name ? facility.street_2_name : '' + facility.street_2_number ? facility.street_2_number?.toString() : '' + ' ' + facility.street_2_direction ? facility.street_2_direction : ''
      const country = facility.country ? facility.country : ''
      const state = facility.governing_district ? facility.governing_district : ''
      const city = facility.city_town ? facility.city_town : ''
      const postal = facility.postal_area ? facility.postal_area?.toString() : ''
      const location = street1 + ' ' + street2 + ' ' + city + ' ' + state + ' ' + postal + ' ' + country
      const out = location.replaceAll(/ /g, '+')
      return out
    },
    formatPhoneNumber: function (phoneNumber) {
      const cleaned = ('' + phoneNumber).replace(/\D/g, '')
      const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
      if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3]
      }
      return null
    },
    activeSection: function (section) {
      if (this.edit_org || this.edit_names || this.edit_supplier_risk_assessment) {
        if (section === 'org_data') {
          return this.edit_org
        }
        if (section === 'names') {
          return this.edit_names
        }
        if (section === 'supplier_risk_assessment') {
          return this.edit_supplier_risk_assessment
        }
        return !(this.edit_org || this.edit_names || this.edit_supplier_risk_assessment)
      }
      return true
    },
    setOrgBuffer: function () {
      this.edit_org_buffer = cloneDeep(this.org_data)
      this.edit_org = true
    },
    submit: async function () {
      this.loaded = false
      const createToast = this.$root.createToast

      const org = {
        organization_id: this.edit_org_buffer.organization_id,
        vetted: this.edit_org_buffer.vetted,
        risk_level: this.edit_org_buffer.risk_level,
        notes: this.edit_org_buffer.notes,
        website_url: this.edit_org_buffer.website_url,
        supplier: this.edit_org_buffer.supplier,
        client: this.edit_org_buffer.client,
        lab: this.edit_org_buffer.lab,
        courier: this.edit_org_buffer.courier,
        other: this.edit_org_buffer.other
      }

      this.req.upsertRecord('Organizations', org)

      const resp = await this.req.sendRequest(window.origin)

      console.error('Request Error: ', resp)
      resp.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp.status !== 201) {
        return false
      }

      this.edit_org = false
      this.getOrganization()
      return true
    },
    cancel: function () {
      this.org_data = cloneDeep(this.edit_org_buffer)
      this.edit_org = false
    },
    toggleLoaded: function (val) {
      this.loaded = val
    },
    refreshParent: function (val) {
      this.getOrganization()
    },
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    getOrganization: function () {
      const fetchRequest = window.origin + '/api/v1/organizations?org-id=' + this.id + '&populate=facilities&populate=people&populate=products&populate=organization_names&populate=components'
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
            this.org_data = data.data[0]
            // eslint-disable-next-line
            console.log(this.org_data)
            this.loaded = true
            this.sorted_people = this.org_data.people.sort(this.sortPeople)
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
    this.getOrganization()
  }
}
</script>

<style scoped>
.card {
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
