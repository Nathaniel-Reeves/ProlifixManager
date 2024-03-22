<template>
  <div>
    <h3 id="Aliases">Aliases<b-button v-show="!edit_names" v-b-tooltip.hover :title="'Edit ' + naming_type + ' names.'" v-on:click="editNames()" v-bind:class="['btn', 'p-1', 'ml-2', 'btn-light']" type="button"><i class="bi bi-pencil-square"></i></b-button></h3>
    <div v-for="name in names" :key="name.name_id">
      <p v-show="!edit_names" v-bind:class="{ bold: name.primary_name, italic: name.botanical_name }">
        {{ getName(name) }}<b-badge variant="primary" pill class="ml-2" style="font-size:1em;" v-show="name.primary_name">Primary</b-badge><b-badge variant="success" pill class="ml-2" style="font-size:1em;" v-show="name.botanical_name">Botanical</b-badge>
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
        <div v-on:click="radioNames(name.name_id, 'primary')">
          <b-form-checkbox :disabled="name.primary_name" button button-variant="light" name="Primary Name" class="mb-2 mr-sm-2 mb-sm-0" v-model="name.primary_name">Primary Name</b-form-checkbox>
        </div>
        <div v-show="'botanical_name' in name" v-on:click="radioNames(name.name_id, 'botanical')">
          <b-form-checkbox button button-variant="light" name="Botanical Name" class="mb-2 mr-sm-2 mb-sm-0" v-model="name.botanical_name">Botanical Name</b-form-checkbox>
        </div>
        <div>
          <b-button variant="outline-danger" class="mb-2 mr-sm-2 mb-sm-0" v-show="!name.primary_name" v-on:click="deleteName(name.name_id)">Delete</b-button>
        </div>
      </b-form>
    </div>
    <div class="d-flex">
      <div v-show="edit_names">
        <b-button variant="outline-info" class="m-2" v-on:click="addName()">New Name</b-button>
        <b-button variant="outline-info" class="m-2" v-on:click="cancelEditNames()">Cancel</b-button>
        <b-button type="submit" v-show="edit_names_buffer.length > 0" variant="primary" class="m-2" v-on:click="editNames()">Save</b-button>
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
export default {
  name: 'NamesComponent',
  props: {
    data: Array,
    saveFunction: Function,
    namingType: String
  },
  data: function () {
    return {
      names: this.data,
      naming_type: this.namingType,
      edit_names: false,
      edit_names_buffer: []
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
    editNames: function () {
      const original = structuredClone(this.names) // Deep Copy
      if (!this.edit_names) {
        this.edit_names_buffer = structuredClone(this.names) // Deep Copy
        this.edit_names = true
      } else {
        this.names = []
        this.names = structuredClone(this.edit_names_buffer) // Deep Copy
        if (this.naming_type === 'component') {
          this.$parent.component_data.Component_Names = structuredClone(this.edit_names_buffer) // Deep Copy
        } else {
          throw new Error('Invalid naming_type: "' + this.naming_type + '". Only component is allowed')
        }
        this.saveFunction().then(outcome => {
          if (outcome === true) {
            this.edit_names_buffer = []
            this.edit_names = false
          } else {
            this.names = original
          }
        })
      }
    },
    cancelEditNames: function () {
      this.edit_names_buffer = []
      this.edit_names = false
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
          name_id: (Math.random() + 1).toString(36).substring(7),
          component_id: parseInt(this.$parent.id),
          component_name: '',
          primary_name: false,
          botanical_name: false
        }
        return newName
      } else {
        throw new Error('Invalid naming_type: "' + this.naming_type + '". Only component is allowed')
      }
    }
  }
}
</script>
