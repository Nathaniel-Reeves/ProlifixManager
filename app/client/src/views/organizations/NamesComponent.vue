<template>
  <div>
    <h3 id="Aliases">Aliases<b-button v-show="!edit_names && allow_edit" v-b-tooltip.hover :title="'Edit ' + naming_type + ' names.'" v-on:click="editNames()" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
    <div v-for="name in names" :key="name.name_id">
      <p v-show="!edit_names" v-bind:class="{ bold: name.primary_name }">
        {{ getName(name) }} {{ getInitial(name) }}<b-badge variant="primary" pill class="ml-2" style="font-size:1em;" v-show="name.primary_name">Primary</b-badge>
      </p>
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
            :class="['form-control', (name.organization_initial?.length > 0 || name.organization_initial?.length < 7 ? '' : 'is-invalid')]"
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
    <div class="d-flex">
      <div v-show="edit_names">
        <b-button variant="outline-info" class="m-2" v-on:click="addName()">New Name</b-button>
        <b-button variant="outline-danger" class="m-2" v-on:click="cancelEditNames()">Cancel</b-button>
        <b-button type="outline-submit" :disabled="edit_names_buffer.length <= 0" variant="success" class="m-2" v-on:click="editNames()">Save</b-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bold {
    font-weight: bold;
}
.italic {
    font-style: italic;
}
.normal {
    font-weight: normal;
}
</style>

<script>
import { cloneDeep } from 'lodash'
import { CustomRequest, genTempKey, isTempKey } from '../../common/CustomRequest.js'

export default {
  name: 'NamesComponent',
  props: {
    pNames: Array,
    namingType: String,
    allowEdit: Boolean,
    id: Number
  },
  data: function () {
    return {
      names: [],
      naming_type: this.namingType,
      allow_edit: this.allowEdit,
      edit_names: false,
      edit_names_buffer: [],
      req: new CustomRequest(this.$cookies.get('session'))
    }
  },
  methods: {
    editNames: async function () {
      if (!this.edit_names) {
        this.edit_names_buffer = cloneDeep(this.names)
        this.edit_names = true
        this.$emit('editNames', this.edit_names)
      } else {
        const createToast = this.$root.createToast
        let newPrimary = null
        let primaryTempKey = false
        this.$emit('toggleLoaded', false)

        this.edit_names_buffer.forEach(name => {
          this.req.upsertRecord('Organization_Names', name)
          if (name.primary_name) {
            newPrimary = name.name_id
          }
          if (isTempKey(name.name_id)) {
            primaryTempKey = true
          }
        })

        if (!primaryTempKey) {
          this.req.upsertRecord('Organizations', { organization_id: this.id, primary_name_id: newPrimary })
        }

        const resp1 = await this.req.sendRequest(window.origin)

        if (resp1.status !== 201) {
          console.error('Request Error: ', resp1)
          resp1.messages.flash.forEach(message => {
            createToast(message)
          })
          return false
        }

        if (!primaryTempKey) {
          resp1.messages.flash.forEach(message => {
            createToast(message)
          })
          this.$parent.refreshParent()
          return true
        }

        const tempKeyLookup = this.req.getTempKeyLookup()
        console.log('TempKeyLookup', tempKeyLookup)
        console.log('newPrimary', newPrimary)

        this.req = new CustomRequest(this.$cookies.get('session'))

        this.req.upsertRecord('Organizations', { organization_id: this.id, primary_name_id: tempKeyLookup[newPrimary].new_id })
        const resp2 = await this.req.sendRequest(window.origin)

        resp2.messages.flash.forEach(message => {
          createToast(message)
        })

        if (resp2.status === 201) {
          this.$parent.refreshParent()
          this.cancelEditNames()
          return true
        }
        return false
      }
    },
    cancelEditNames: function () {
      this.edit_names_buffer = []
      this.edit_names = false
      this.$emit('editNames', this.edit_names)
      this.req = new CustomRequest(this.$cookies.get('session'))
    },
    getName: function (name) {
      if (this.naming_type === 'component') {
        return name.component_name
      } else {
        return name.organization_name
      }
    },
    getInitial: function (name) {
      return name.organization_initial
    },
    getObjNameId: function (name) {
      if (this.naming_type === 'component') {
        return name.component_id
      } else {
        return name.organization_id
      }
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
          if (isTempKey(this.edit_names_buffer[i].name_id)) {
            this.req.removeUpsertRecord('Organization_Names', 'name_id', this.edit_names_buffer[i].name_id)
          } else {
            this.req.deleteRecord('Organization_Names', { name_id: this.edit_names_buffer[i].name_id })
          }
          this.edit_names_buffer.splice(i, 1)
        }
      }
    },
    createName: function () {
      const newName = {
        name_id: genTempKey(),
        organization_id: this.id,
        organization_name: null,
        organization_initial: null,
        primary_name: false
      }
      return newName
    }
  },
  created: function () {
    this.names = this.pNames
  }
}
</script>
