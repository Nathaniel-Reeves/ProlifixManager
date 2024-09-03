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
                <h1>{{ person.first_name }} {{ person.last_name }}</h1>
              </div>
              <router-link :to="'/organizations/'+person.organization_id" target="_blank"><h4 class="card-subtitle text-muted mb-2">{{ person.organizations[0].organization_primary_name }} {{ person.organizations[0].organization_primary_initial ? '(' + person.organizations[0].organization_primary_initial + ')' : '' }}</h4></router-link>
            </div>
          </div>
          <hr class="d-print-none">
          <b-nav pills card-header slot="header" v-b-scrollspy:nav-scroller class="text-nowrap d-print-none">
            <b-nav-item href="#PersonalInfo">Personal Info</b-nav-item>
            <b-nav-item href="#ContactDetails">Contact Details</b-nav-item>
            <b-nav-item href="#JobDetails">Job Details</b-nav-item>
          </b-nav>
        </b-card-body>
      </b-card>

      <b-card class="my-2" v-if="loaded">
        <b-card-body id="nav-scroller" ref="content" class="scrollbox">
          <h3 id="PersonalInfo">Personal Info<b-button v-if="!edit" v-b-tooltip.hover title="Edit Person" @click="toggleEdit()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <div>
            <b-row>
              <b-col style="max-width:15%;"><label for="first_name"><strong>First Name:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="first_name"
                    type="text"
                    v-model="person.first_name"
                    required
                    :disabled="!edit"
                    aria-describedby="first_name-live-feedback"
                    :class="['form-control', (person.first_name ? '' : 'is-invalid')]"
                    @input="update()"
                    v-on:keyup.enter="focus('last_name')"
                  >
                  <div id="first_name-live-feedback" class="invalid-feedback">This required field.</div>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:15%;"><label for="last_name"><strong>Last Name:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="last_name"
                    type="text"
                    v-model="person.last_name"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('birthday')"
                  >
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:15%;"><label for="birthday"><strong>Birthday:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <b-form-datepicker
                    id="birthday"
                    type="text"
                    v-model="person.birthday"
                    required
                    :disabled="!edit"
                    :max="new Date()"
                    :readonly="!edit"
                    @input="update()"
                    v-on:keyup.enter="focus('email_address_primary')"
                  ></b-form-datepicker>
                </div>
              </b-col>
            </b-row>
          </div>
          <hr>
          <h3 id="ContactDetails">Contact Details<b-button v-if="!edit" v-b-tooltip.hover title="Edit Person" @click="toggleEdit()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <div>
            <b-row>
              <b-col style="max-width:23%;"><label for="email_address_primary"><strong>Primary Email:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="email_address_primary"
                    type="email"
                    v-model="person.email_address_primary"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('email_address_secondary')"
                  >
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:23%;"><label for="email_address_secondary"><strong>Secondary Email:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="email_address_secondary"
                    type="email"
                    v-model="person.email_address_secondary"
                    required
                    :disabled="!edit"
                    @input="update()"
                    class="form-control"
                    v-on:keyup.enter="focus('phone_number_primary')"
                  >
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:23%;"><label for="phone_number_primary"><strong>Primary Phone Number:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    v-show="edit"
                    id="phone_number_primary"
                    type="tel"
                    v-model="person.phone_number_primary"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('phone_number_secondary')"
                  >
                  <input
                    v-show="!edit"
                    type="tel"
                    :placeholder="formatPhoneNumber(person.phone_number_primary)"
                    required
                    disabled
                    class="form-control"
                  >
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:23%;"><label for="phone_number_secondary"><strong>Secondary Phone Number:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    v-show="edit"
                    id="phone_number_secondary"
                    type="tel"
                    v-model="person.phone_number_secondary"
                    required
                    :disabled="!edit"
                    class="form-control"
                    @input="update()"
                    v-on:keyup.enter="focus('first_name')"
                  >
                  <input
                    v-show="!edit"
                    type="tel"
                    :placeholder="formatPhoneNumber(person.phone_number_secondary)"
                    required
                    disabled
                    class="form-control"
                  >
                </div>
              </b-col>
            </b-row>
          </div>
          <hr>
          <h3 id="JobDetails">Job Details<b-button v-if="!edit" v-b-tooltip.hover title="Edit Person" @click="toggleEdit()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
          <div>
            <b-row v-if="person.organization_id === 1" class="mb-3">
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
            </b-row>
            <b-row v-if="person.organization_id === 1 && person.is_employee">
              <b-col style="max-width:23%;"><label for="contract_date"><strong>Contract Date:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <b-form-datepicker
                    id="contract_date"
                    v-model="person.contract_date"
                    required
                    :disabled="!edit"
                    :max="new Date()"
                    :readonly="!edit"
                    @input="update()"
                    v-on:keyup.enter="focus('first_name')"
                  ></b-form-datepicker>
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:23%;"><label for="department"><strong>Department/s:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="department"
                    type="text"
                    v-model="person.department"
                    :disabled="!edit"
                    @input="update()"
                    class="form-control"
                    v-on:keyup.enter="focus('job_description')"
                  >
                </div>
              </b-col>
            </b-row>
            <b-row>
              <b-col style="max-width:23%;"><label for="job_description"><strong>Job/s:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <input
                    id="job_description"
                    type="text"
                    v-model="person.job_description"
                    :disabled="!edit"
                    @input="update()"
                    class="form-control"
                    v-on:keyup.enter="focus('department')"
                  >
                </div>
              </b-col>
            </b-row>
            <b-row v-if="person.organization_id === 1 && person.is_employee">
              <b-col style="max-width:23%;"><label for="termination_date"><strong>Termination Date:</strong></label></b-col>
              <b-col>
                <div class="input-group mb-2">
                  <b-form-datepicker
                    id="termination_date"
                    v-model="person.termination_date"
                    :disabled="!edit"
                    :max="new Date()"
                    :readonly="!edit"
                    @input="update()"
                    v-on:keyup.enter="focus('first_name')"
                  ></b-form-datepicker>
                </div>
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
import { CustomRequest } from '../../common/CustomRequest.js'
import { cloneDeep } from 'lodash'

export default {
  name: 'PeopleDetail',
  data: function () {
    return {
      id: this.$route.params.id,
      loaded: false,
      edit: false,
      original_person: {},
      person: {},
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    toggleEdit: function () {
      if (!this.edit) {
        this.original_person = cloneDeep(this.person)
      }
      this.edit = !this.edit
    },
    update: function () {
      const person = {
        person_id: this.person.person_id,
        first_name: this.person.first_name,
        last_name: this.person.last_name,
        birthday: this.person.birthday,
        email_address_primary: this.person.email_address_primary,
        email_address_secondary: this.person.email_address_secondary,
        phone_number_primary: this.person.phone_number_primary,
        phone_number_secondary: this.person.phone_number_secondary,
        department: this.person.department,
        job_description: this.person.job_description,
        is_employee: this.person.is_employee,
        contract_date: this.person.contract_date,
        termination_date: this.person.termination_date,
        timestamp_fetched: this.person.timestamp_fetched
      }
      this.req.updateUpsertRecord('People', 'person_id', this.person.person_id, person)
    },
    validate: function () {
      this.$bvToast.hide()

      const errorToast = {
        title: 'Invalid Person',
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

      if (!this.person.first_name) {
        errorToast.message = 'Person must have a first name.'
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
        this.edit = false
        this.loaded = false
        this.getPerson()
      } else {
        this.$root.handleStaleRequest(this.req.isStale(), window.location)
        this.edit = false
        this.loaded = true
      }
    },
    cancel: function () {
      this.person = cloneDeep(this.original_person)
      this.edit = false
    },
    formatPhoneNumber: function (phoneNumber) {
      const cleaned = ('' + phoneNumber).replace(/\D/g, '')
      const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
      if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3]
      }
      return null
    },
    scrollIntoView: function (event) {
      event.preventDefault()
      const href = event.target.getAttribute('href')
      const el = href ? document.querySelector(href) : null
      if (el) {
        this.$refs.content.scrollTop = el.offsetTop
      }
    },
    getPerson: function () {
      const fetchRequest = this.$root.getOrigin() + '/api/v1/organizations/people?person_id=' + this.id + '&populate=organizations'
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
            this.person = data.data[0]
            // eslint-disable-next-line
            console.log(this.person)
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
    this.getPerson()
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
