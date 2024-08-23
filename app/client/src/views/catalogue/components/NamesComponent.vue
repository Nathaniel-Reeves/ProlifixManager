<template>
  <div>
    <h3 id="Aliases" v-show="!hideHeader">Aliases<b-button v-show="!edit_names && allow_edit" v-b-tooltip.hover :title="'Edit ' + naming_type + ' names.'" v-on:click="editNames()" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>
    <div v-for="name in names" :key="name.name_id">
      <p v-show="!edit_names" :class="[ name.primary_name ? 'bold' : '', hideHeader ? 'ml-3' : '' ]">
        {{ hideHeader ? '- ' : '' }}{{ getName(name) }}<b-badge variant="primary" pill class="ml-2" style="font-size:1em;" v-show="name.primary_name">Primary</b-badge><b-badge variant="success" pill class="ml-2" style="font-size:1em;" v-show="name.botanical_name">Botanical</b-badge>
      </p>
    </div>
    <div v-for="name in edit_names_buffer" :key="'edit' + name.name_id">
      <b-form inline v-show="edit_names" class="m-2" @submit.stop.prevent>
        <label class="sr-only" for="inline-form-input-name">name</label>
        <b-form-input
          id="inline-form-input-name"
          class="mb-2 mr-sm-2 mb-sm-0"
          v-model="name.component_name"
          ></b-form-input>
        <div class="btn-group-toggle d-inline-block mb-2 mr-sm-2 mb-sm-0">
          <label :class="['btn', name.primary_name ? 'btn-primary' : 'btn-outline-primary', name.primary_name ? 'disabled' : '']">
            <input v-on:click="radioNames(name.name_id, 'primary')" type="checkbox" name="Primary Name" :disabled="name.primary_name" v-model="name.primary_name">Primary Name
          </label>
        </div>
        <div v-show="'botanical_name' in name" class="btn-group-toggle d-inline-block mb-2 mr-sm-2 mb-sm-0">
          <label :class="['btn', name.botanical_name ? 'btn-success' : 'btn-outline-success', name.botanical_name ? 'disabled' : '']">
            <input v-on:click="radioNames(name.name_id, 'botanical')" type="checkbox" name="Botanical Name" :disabled="name.botanical_name" v-model="name.botanical_name">Botanical Name
          </label>
        </div>
        <div>
          <b-button variant="outline-danger" class="mb-2 mr-sm-2 mb-sm-0" v-show="!name.primary_name" v-on:click="deleteName(name.name_id)">Delete</b-button>
        </div>
      </b-form>
    </div>
    <div class="d-flex">
      <div v-show="edit_names">
        <b-button variant="outline-info" class="m-2" v-on:click="addName()">New Name</b-button>
        <b-button variant="outline-danger" class="m-2" v-on:click="cancelEditNames()">Cancel</b-button>
        <b-button type="submit" :disabled="edit_names_buffer.length <= 0" variant="outline-success" class="m-2" v-on:click="editNames()">Save</b-button>
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
import { CustomRequest, genTempKey, isTempKey } from '../../../common/CustomRequest.js'

export default {
  name: 'NamesComponent',
  props: {
    pNames: Array,
    namingType: String,
    allowEdit: Boolean,
    id: Number,
    timestampFetched: String,
    hideHeader: {
      type: Boolean,
      default: false
    }
  },
  data: function () {
    return {
      names: [],
      naming_type: this.namingType,
      allow_edit: this.allowEdit,
      edit_names: false,
      edit_names_buffer: [],
      req: this.allowEdit ? new CustomRequest(this.$cookies.get('session')) : null
    }
  },
  methods: {
    radioNames: function (id, flag) {
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].name_id === id) {
          continue
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
    editNames: async function () {
      if (!this.edit_names) {
        this.edit_names_buffer = cloneDeep(this.names)
        this.edit_names = true
        this.$emit('editNames', this.edit_names)
      } else {
        if (this.naming_type === 'component') {
          let primary = null
          this.edit_names_buffer.forEach(name => {
            this.req.upsertRecord('Component_Names', name)
            if (name.primary_name) {
              primary = name.name_id
              this.req.upsertRecord('Components', { component_id: this.id, primary_name_id: primary, timestamp_fetched: this.timestampFetched })
            }
          })
        } else {
          throw new Error('Invalid naming_type: "' + this.naming_type + '". Only component is allowed')
        }

        this.req.setUpsertOrder(['Component_Names', 'Components'])

        const resp = await this.req.sendRequest(window.origin)
        this.$emit('toggleLoaded', false)

        const createToast = this.$root.createToast
        resp.messages.flash.forEach(message => {
          createToast(message)
        })

        const hsr = this.$root.handleStaleRequest
        hsr(this.req.isStale(), window.location)

        if (resp.status === 201) {
          this.cancelEditNames()
          this.$emit('refreshParent')
        }
      }
    },
    cancelEditNames: function () {
      this.edit_names_buffer = []
      this.edit_names = false
      this.$emit('editNames', this.edit_names)
      this.req = new CustomRequest(this.$cookies.get('session'))
    },
    addName: function () {
      const newName = this.createName()
      this.edit_names_buffer.push(newName)
    },
    deleteName: function (id) {
      for (let i = 0; i < this.edit_names_buffer.length; i++) {
        if (this.edit_names_buffer[i].name_id === id) {
          this.edit_names_buffer.splice(i, 1)
          if (!isTempKey(id)) {
            this.req.deleteRecord('Component_Names', { name_id: id })
          }
        }
      }
    },
    getName: function (name) {
      if (this.naming_type === 'component') {
        return name.component_name
      } else {
        throw new Error('Invalid naming_type: "' + this.naming_type + '". Only component is allowed')
      }
    },
    getObjNameId: function (name) {
      if (this.naming_type === 'component') {
        return name.component_id
      }
    },
    createName: function () {
      if (this.naming_type === 'component') {
        const newName = {
          name_id: genTempKey(),
          component_id: this.id,
          component_name: '',
          primary_name: false,
          botanical_name: false,
          timestamp_fetched: new Date().toISOString()
        }
        return newName
      } else {
        throw new Error('Invalid naming_type: "' + this.naming_type + '". Only component is allowed')
      }
    }
  },
  created: function () {
    this.names = this.pNames
  }
}
</script>
