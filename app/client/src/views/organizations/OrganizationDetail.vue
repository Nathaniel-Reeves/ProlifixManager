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
            <h2 class="card-title">{{ org_data.organization_primary_name }} {{ '(' + org_data.organization_primary_initial + ')' }}
              <b-badge v-show="org_data.supplier" variant="light" class="mr-2 border">Supplier</b-badge>
              <b-badge v-show="org_data.client" variant="light" class="mr-2 border">Client</b-badge>
              <b-badge v-show="org_data.lab" variant="light" class="mr-2 border">Lab</b-badge>
              <b-badge v-show="org_data.courier" variant="light" class="mr-2 border">Courier</b-badge>
              <b-badge v-show="org_data.other" variant="light" class="mr-2 border">Other</b-badge>
            </h2>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#GeneralInfo" @click="scrollIntoView" :disabled="edit_names">General Info</b-nav-item>
            <b-nav-item href="#Aliases" @click="scrollIntoView" :disabled="edit_org">Aliases</b-nav-item>
            <b-nav-item href="#Products" @click="scrollIntoView" :disabled="edit_org || edit_names" v-show="org_data.client">Products</b-nav-item>
            <b-nav-item href="#Components" @click="scrollIntoView" :disabled="edit_org || edit_names" v-show="org_data.supplier">Components</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class=" my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">

          <!-- General Info -->
          <div v-show="!edit_names">
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

            <div class="d-flex mb-3">
              <strong class='mr-3'>Risk Level: </strong>
              <div v-if="edit_org">
                <b-form-group>
                  <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
                    <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_0" value="UNKNOWN" v-model="edit_org_buffer.risk_level">
                    <label class="custom-control-label" for="risk_level_0"><b-badge variant="light">Unknown</b-badge></label>
                  </div>
                  <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
                    <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_2" value="Low_Risk" v-model="edit_org_buffer.risk_level">
                    <label class="custom-control-label" for="risk_level_2"><b-badge variant="success">Low Risk</b-badge></label>
                  </div>
                  <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
                    <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_3" value="Medium_Risk" v-model="edit_org_buffer.risk_level">
                    <label class="custom-control-label" for="risk_level_3"><b-badge variant="warning">Medium Risk</b-badge></label>
                  </div>
                  <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
                    <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_4" value="High_Risk" v-model="edit_org_buffer.risk_level">
                    <label class="custom-control-label" for="risk_level_4"><b-badge variant="danger">High Risk</b-badge></label>
                  </div>
                </b-form-group>
              </div>
              <h3 v-else>
                <b-badge v-show="org_data.risk_level === 'UNKNOWN'" variant="light" class="mr-2 border">Unknown</b-badge>
                <b-badge v-show="org_data.risk_level === 'Low_Risk' || org_data.risk_level === 'No_Risk'" variant="success" class="mr-2 border">Low Risk</b-badge>
                <b-badge v-show="org_data.risk_level === 'Medium_Risk'" variant="warning" class="mr-2 border">Medium Risk</b-badge>
                <b-badge v-show="org_data.risk_level === 'High_Risk'" variant="danger" class="mr-2 border">High Risk</b-badge>
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
              <b-form-group>
                <b-form-input
                  :disabled="!edit_org"
                  id="website_url"
                  v-model="edit_org_buffer.website_url"
                  placeholder="Enter website URL"
                  type="url"
                ></b-form-input>
              </b-form-group>
            </div>

            <div class="d-flex">
              <div v-show="edit_org">
                <b-button variant="danger" class="m-2" v-on:click="cancel()">Cancel</b-button>
                <b-button type="submit" variant="success" class="m-2" v-on:click="submit()">Save</b-button>
              </div>
            </div>
          </div>
          <hr v-show="!edit_org">

          <!-- Alias Names -->
          <NamesComponent
            v-show="!edit_org"
            :p-names="org_data.organization_names"
            :id="org_data.organization_id"
            naming-type="organization"
            :allow-edit="true"
            v-on:edit-names="(e) => edit_names = e"
            v-on:toggle-loaded="toggleLoaded"
            v-on:refresh-parent="refreshParent"
          ></NamesComponent>
          <hr v-show="!edit_org && !edit_names && org_data.client">

          <!-- Products -->
          <div v-show="!edit_org && !edit_names && org_data.client">
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
          <hr v-show="!edit_org && !edit_names && org_data.supplier">

          <!-- Components -->
          <div v-show="!edit_org && !edit_names && org_data.supplier">
            <h3 id="Components">Components</h3>
            <b-table striped :items="org_data.components" show-empty id="components-table" :per-page="perPage" :current-page="currentComponentPage" bordered
              :fields="[
                { key: 'component_primary_name', label: 'Component', thStyle: { width: '40%' } },
                { key: 'certs', label: 'Certs' }
              ]">
              <template #cell(component_primary_name)="data">
                <b-button v-on:click.stop class="mr-2" variant="light" :to="'/catalogue/components/'+data.item.product_id " target="_blank"><b-icon icon="box"></b-icon></b-button>
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

export default {
  name: 'OrganizationDetail',
  components: {
    NamesComponent,
    CertBadge
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
      edit_org_buffer: {},
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
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
      const fetchRequest = window.origin + '/api/v1/organizations?org-id=' + this.id + '&populate=facilities&populate=people&populate=products&populate=organization_names'
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
