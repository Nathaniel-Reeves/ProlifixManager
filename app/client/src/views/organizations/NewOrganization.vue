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
        <h2 class="card-title flex-grow-1">New Organization Form</h2>

        <b-form>
          <div class="d-flex justify-content-between mt-3 mb-0">
            <p><strong>Aliases</strong></p>
            <b-button variant="outline-info" class="m-2" v-on:click="addName()">New Name</b-button>
          </div>
          <div v-for="name in edit_names_buffer" :key="'edit' + name.name_id">
            <div class="mb-2 d-flex">
              <label class="sr-only" for="inline-form-input-name">name</label>
              <div class="mb-2 mr-sm-2 mb-sm-0" style="width:50%;">
                <b-form-input
                  required
                  v-model="name.organization_name"
                  placeholder="Organization Name"
                  aria-describedby="inline-form-input-name-live-feedback"
                  :class="['form-control', (name.organization_name && name.organization_name?.length > 0 ? '' : 'is-invalid')]"
                ></b-form-input>
                <div id="inline-form-input-name-live-feedback" class="invalid-feedback">This is a required field.</div>
              </div>
              <div class="mb-2 mr-sm-2 mb-sm-0" style="width:20%;">
                <b-form-input
                  required
                  v-model="name.organization_initial"
                  placeholder="Initials"
                  aria-describedby="inline-form-input-initial-live-feedback"
                  :class="['form-control', (name.organization_initial && name.organization_initial?.length <= 10 ? '' : 'is-invalid')]"
                ></b-form-input>
                <div id="inline-form-input-initial-live-feedback" class="invalid-feedback">This is a required field that must be no longer than 10 characters.</div>
              </div>
              <div>
                <b-button @click="radioNames(name.name_id, 'primary')" :disabled="name.primary_name" :pressed="name.primary_name" :variant="name.primary_name ? 'primary' : 'outline-primary'" class="mb-2 mr-sm-2 mb-sm-0">Primary Name</b-button>
              </div>
              <div>
                <b-button variant="outline-danger" class="mb-2 mr-sm-2 mb-sm-0" v-show="!name.primary_name" v-on:click="deleteName(name.name_id)">Delete</b-button>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-between mt-3 mb-0">
            <p><strong>Organization Type</strong></p>
          </div>
          <b-form-group aria-describedby="organization-type-live-feedback" :class="[ ( org_buffer.supplier || org_buffer.client || org_buffer.lab || org_buffer.courier || org_buffer.other ? '' : 'is-invalid')]">
            <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
              <input class="custom-control-input" type="checkbox" name="supplier" id="supplier" v-model="org_buffer.supplier">
              <label class="custom-control-label" for="supplier">Supplier</label>
            </div>
            <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
              <input class="custom-control-input" type="checkbox" name="client" id="client" v-model="org_buffer.client">
              <label class="custom-control-label" for="client">Client</label>
            </div>
            <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
              <input class="custom-control-input" type="checkbox" name="lab" id="lab" v-model="org_buffer.lab">
              <label class="custom-control-label" for="lab">Laboratory</label>
            </div>
            <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
              <input class="custom-control-input" type="checkbox" name="courier" id="courier" v-model="org_buffer.courier">
              <label class="custom-control-label" for="courier">Courier</label>
            </div>
            <div class="custom-control custom-control-inline custom-checkbox b-custom-control-lg">
              <input class="custom-control-input" type="checkbox" name="other" id="other" v-model="org_buffer.other">
              <label class="custom-control-label" for="other">Other</label>
            </div>
          </b-form-group>
          <div id="organization-type-live-feedback" class="invalid-feedback">At least one organization type must be selected.</div>

          <!-- <div class="d-flex justify-content-between mt-3 mb-0">
            <p><strong>Risk Level</strong></p>
          </div>
          <b-form-group>
            <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
              <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_0" value="UNKNOWN" v-model="org_buffer.risk_level">
              <label class="custom-control-label" for="risk_level_0"><b-badge variant="light">Unknown</b-badge></label>
            </div>
            <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
              <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_2" value="Low_Risk" v-model="org_buffer.risk_level">
              <label class="custom-control-label" for="risk_level_2"><b-badge variant="success">Low Risk</b-badge></label>
            </div>
            <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
              <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_3" value="Medium_Risk" v-model="org_buffer.risk_level">
              <label class="custom-control-label" for="risk_level_3"><b-badge variant="warning">Medium Risk</b-badge></label>
            </div>
            <div class="custom-control custom-control-inline custom-radio b-custom-control-lg">
              <input class="custom-control-input" type="radio" name="risk_level" id="risk_level_4" value="High_Risk" v-model="org_buffer.risk_level">
              <label class="custom-control-label" for="risk_level_4"><b-badge variant="danger">High Risk</b-badge></label>
            </div>
          </b-form-group> -->

          <div class="d-flex justify-content-between mt-3 mb-0">
            <p><strong>Notes</strong></p>
          </div>
          <b-form-group>
            <b-form-textarea
              id="textarea"
              v-model="org_buffer.notes"
              placeholder="Enter notes here..."
              rows="3"
              max-rows="6"
            ></b-form-textarea>
          </b-form-group>

          <div class="d-flex justify-content-between mt-3 mb-0">
            <p><strong>Website</strong></p>
          </div>
          <b-form-group>
            <b-form-input
              id="website_url"
              v-model="org_buffer.website_url"
              placeholder="Enter website URL"
              type="url"
            ></b-form-input>
          </b-form-group>

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
import { CustomRequest, genTempKey } from '../../common/CustomRequest.js'
import orgDoc from './orgDocTemp.js'
import NamesComponent from './NamesComponent.vue'
import { BBadge, BLink } from 'bootstrap-vue'

export default {
  name: 'NewOrganization',
  components: [
    NamesComponent,
    BBadge,
    BLink
  ],
  data: function () {
    return {
      loaded: true,
      new_org_id: null,
      edit_names_buffer: [],
      org_buffer: {
        organization_id: this.new_org_id,
        website_url: null,
        vetted: false,
        date_vetted: null,
        risk_level: 'UNKNOWN',
        supplier: false,
        client: false,
        lab: false,
        courier: false,
        other: false,
        notes: null,
        doc: orgDoc,
        flash_errors: [],
        duplicate_flag: null
      },
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
    buildDuplicateModalMessage: function (testName, score, potentialDuplicate) {
      console.log('potentialDuplicate:', potentialDuplicate)
      const h = this.$createElement
      const messageVNode = h('div', [
        h('p', [
          `'${testName}' (new organization) has a ${score}% match with '${potentialDuplicate.organization_name}' (pre-existing organization).  Are these two organizations the same?`
        ]),
        h('p', [
          `If so, click YES to go to the '${potentialDuplicate.organization_name}' spec page.`
        ]),
        h('p', [
          'If not, click NO to continue creating the new organization.'
        ]),
        potentialDuplicate.organization_names.length > 0 ? h('p', ['The following information is associated with the existing organization:']) : null,
        h('div', [
          potentialDuplicate.organization_names.length > 0 ? h(NamesComponent, { props: { pNames: potentialDuplicate.organization_names, namingType: 'organization', allowEdit: false, id: potentialDuplicate.organization_id, hideHeader: true } }) : null
        ]),
        h('p', [
          'Type: ',
          potentialDuplicate.supplier ? h(BBadge, { variant: 'light', class: ['mr-2', 'border'] }, ['Supplier']) : null,
          potentialDuplicate.client ? h(BBadge, { variant: 'light', class: ['mr-2', 'border'] }, ['Client']) : null,
          potentialDuplicate.lab ? h(BBadge, { variant: 'light', class: ['mr-2', 'border'] }, ['Lab']) : null,
          potentialDuplicate.courier ? h(BBadge, { variant: 'light', class: ['mr-2', 'border'] }, ['Courier']) : null,
          potentialDuplicate.other ? h(BBadge, { variant: 'light', class: ['mr-2', 'border'] }, ['Other']) : null
        ]),
        h('p', [
          'Risk Status: ',
          potentialDuplicate.risk_level === 'UNKNOWN' ? h(BBadge, { variant: 'danger', class: ['mr-2', 'border'] }, ['Unknown Risk']) : null,
          potentialDuplicate.risk_level === 'Low_Risk' || potentialDuplicate.risk_level === 'No_Risk' ? h(BBadge, { variant: 'success', class: ['mr-2', 'border'] }, ['Low Risk']) : null,
          potentialDuplicate.risk_level === 'Medium_Risk' ? h(BBadge, { variant: 'warning', class: ['mr-2', 'border'] }, ['Medium Risk']) : null,
          potentialDuplicate.risk_level === 'High_Risk' ? h(BBadge, { variant: 'danger', class: ['mr-2', 'border'] }, ['High Risk']) : null
        ]),
        h('p', [
          'Website: ',
          h(BLink, { exact: true, class: ['text-info'], attrs: { href: this.buildURL(potentialDuplicate.website_url), target: '_blank' } }, [potentialDuplicate.website_url])
        ])
      ])
      return messageVNode
    },
    handleDuplicates: async function (data) {
      this.duplicate_flag = false
      for (let i = 0; i < data.length; i++) {
        for (let j = 0; j < data[i].similar_names.length; j++) {
          const potentialDuplicate = data[i].similar_names[j]
          const testName = data[i].organization_name
          const testInitial = data[i].organization_initial
          const nameScore = data[i].similar_names[j].duplicate_probability_score_name
          const initialScore = data[i].similar_names[j].duplicate_probability_score_initial
          const score = nameScore > initialScore ? nameScore : initialScore
          const pickTestName = nameScore > initialScore ? testName : testInitial
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
            [this.buildDuplicateModalMessage(pickTestName, score, potentialDuplicate)], modal
          )
          if (this.duplicate_flag) {
            return false
          }
          if (value) {
            this.duplicate_flag = true
            this.$router.push({ path: `/organizations/${potentialDuplicate.organization_id}` })
            return false
          }
        }
      }
      return true
    },
    checkOrganizationAlreadyExists: async function () {
      const fetchRequest = window.origin + '/api/v1/submit/check_organization'
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
    validateNewOrg: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Formula',
        message: '',
        variant: 'warning',
        visible: true,
        no_close_button: false,
        no_auto_hide: true,
        auto_hide_delay: false
      }
      const createToast = this.$root.createToast

      if (this.edit_names_buffer.length === 0) {
        errorToast.message = 'At least one name must be provided.'
        createToast(errorToast)
        return false
      }
      let flag = true
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].organization_name?.length === 0) {
          errorToast.message = 'All names must have a name.'
          createToast(errorToast)
          flag = false
        }
        if (this.edit_names_buffer[i].organization_initial?.length === 0) {
          errorToast.message = 'All names must have initials.'
          createToast(errorToast)
          flag = false
        }
        if (this.edit_names_buffer[i].organization_initial?.length > 10) {
          errorToast.message = 'Initials must be no longer than 10 characters.'
          createToast(errorToast)
          flag = false
        }
      }
      if (!(this.org_buffer.supplier || this.org_buffer.client || this.org_buffer.lab || this.org_buffer.courier || this.org_buffer.other)) {
        errorToast.message = 'At least one organization type must be selected.'
        createToast(errorToast)
        flag = false
      }
      return flag
    },
    submit: async function () {
      this.loaded = false
      if (!this.validateNewOrg()) {
        this.loaded = true
        return false
      }

      const result1 = await this.checkOrganizationAlreadyExists()
      if (!result1) {
        return false
      }
      const result2 = await this.handleDuplicates(result1)
      if (!result2) {
        return false
      }

      let primaryNameTempKey = ''

      this.req.upsertRecord('Organizations', this.org_buffer)
      this.edit_names_buffer.forEach(name => {
        name.organization_initial = name.organization_initial.toUpperCase()
        this.req.upsertRecord('Organization_Names', name)
        if (name.primary_name) {
          primaryNameTempKey = name.name_id
        }
      })

      const createToast = this.$root.createToast

      const resp1 = await this.req.sendRequest(window.origin)

      if (resp1.status !== 201) {
        resp1.messages.flash.forEach(message => {
          createToast(message)
        })
        this.loaded = true
        return false
      }

      const tempKeyLookup = this.req.getTempKeyLookup()
      this.req = new CustomRequest(this.$cookies.get('session'))

      const updateOrg = {
        organization_id: tempKeyLookup[this.new_org_id].new_id,
        primary_name_id: tempKeyLookup[primaryNameTempKey].new_id
      }
      this.req.upsertRecord('Organizations', updateOrg)
      const resp2 = await this.req.sendRequest(window.origin)

      resp2.messages.flash.forEach(message => {
        createToast(message)
      })

      if (resp2.status !== 201) {
        this.loaded = true
        return false
      }

      this.$router.push({ path: `/organizations/${updateOrg.organization_id}` })
      return true
    },
    radioNames: function (id) {
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].name_id === id) {
          this.edit_names_buffer[i].primary_name = true
        } else {
          this.edit_names_buffer[i].primary_name = false
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
        organization_id: this.new_org_id,
        organization_name: null,
        organization_initial: null,
        primary_name: false
      }
      return newName
    }
  },
  created: function () {
    this.new_org_id = genTempKey()
    this.org_buffer.organization_id = this.new_org_id
    this.addName()
    this.radioNames(this.edit_names_buffer[0].name_id, 'primary')
  }
}
</script>
