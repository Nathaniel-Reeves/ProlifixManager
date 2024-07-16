<template>
  <div class="my_component">
    <div class="card my-2">
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
                  :class="['form-control', (name.organization_name?.length > 0 ? '' : 'is-invalid')]"
                ></b-form-input>
                <div id="inline-form-input-name-live-feedback" class="invalid-feedback">This is a required field.</div>
              </div>
              <div class="mb-2 mr-sm-2 mb-sm-0" style="width:20%;">
                <b-form-input
                  required
                  v-model="name.organization_initial"
                  placeholder="Initials"
                  aria-describedby="inline-form-input-initial-live-feedback"
                  :class="['form-control', (name.initial?.length > 0 || name.initial?.length < 7 ? '' : 'is-invalid')]"
                ></b-form-input>
                <div id="inline-form-input-initial-live-feedback" class="invalid-feedback">This is a required field that must be no longer than 6 characters.</div>
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

          <div class="d-flex justify-content-between mt-3 mb-0">
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
          </b-form-group>

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

export default {
  name: 'NewOrganization',
  data: function () {
    return {
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
        notes: null
      },
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
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
        if (this.edit_names_buffer[i].organization_initial?.length > 6) {
          errorToast.message = 'Initials must be no longer than 6 characters.'
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
    submit: function () {
      if (!this.validateNewOrg()) {
        return false
      }

      this.req.upsertRecord('Organizations', this.org_buffer)
      this.edit_names_buffer.forEach(name => {
        name.organization_initial = name.organization_initial.toUpperCase()
        this.req.upsertRecord('Organization_Names', name)
      })

      this.req.sendRequest(window.origin).then(resp => {
        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp.status === 201) {
          Object.values(resp.data[0].temp_key_lookup).forEach(item => {
            if (item.table_name === 'Organizations') {
              this.$router.push({ path: `/organizations/${item.new_id}` })
            }
          })
        }
      })
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
