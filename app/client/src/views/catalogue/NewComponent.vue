<template>
  <div class="my_component">
    <div class="card m-2">
      <div class="card-body">
        <h2 class="card-title flex-grow-1">New Component Form</h2>

        <div class="d-flex justify-content-between">
          <p><strong>Aliases</strong></p>
            <b-button variant="outline-info" class="m-2" v-on:click="addName()">New Name</b-button>
        </div>
        <div v-for="name in edit_names_buffer" :key="'edit' + name.name_id">
          <b-form inline class="m-2">
            <label class="sr-only" for="inline-form-input-name">name</label>
            <b-form-input
              id="inline-form-input-name"
              class="mb-2 mr-sm-2 mb-sm-0"
              v-model="name.component_name"
              ></b-form-input>
            <div v-on:click="radioNames(name.name_id, 'primary')">
              <b-form-checkbox button button-variant="light" name="Primary Name" class="mb-2 mr-sm-2 mb-sm-0" v-model="name.primary_name">Primary Name</b-form-checkbox>
            </div>
            <div v-show="component_type === 'powder' || component_type === 'liquid'" v-on:click="radioNames(name.name_id, 'botanical')">
              <b-form-checkbox button button-variant="light" name="Botanical Name" class="mb-2 mr-sm-2 mb-sm-0" v-model="name.botanical_name">Botanical Name</b-form-checkbox>
            </div>
            <div>
              <b-button variant="outline-danger" class="mb-2 mr-sm-2 mb-sm-0" v-show="!name.primary_name" v-on:click="deleteName(name.name_id)">Delete</b-button>
            </div>
          </b-form>
        </div>

        <b-form>
          <b-form-group>
            <label for="description_statement"><strong>Component Type</strong><br></label>
            <b-form-select v-model="component_type" :options="component_options"></b-form-select>
          </b-form-group>

          <b-form-group>
            <label for="description_statement"><strong>Stock Keeping Measure Unit</strong><br></label>
            <b-form-select :disabled="component_type === 'powder' || component_type === 'liquid'" v-model="unit_type" :options="unit_options"></b-form-select>
          </b-form-group>

          <div v-show="component_type === 'powder' || component_type === 'liquid'">
            <label for="description_statement"><strong>Certifications</strong><br></label>
            <div>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_usda_organic">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/usda_organic.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_made_with_organic">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/made_with_organic.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_wildcrafted">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/wildcrafted.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_fda">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/fda_approved.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_gmp">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/good_manufacturing_practice.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_halal">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/halal_certified.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_kosher">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/kosher_certified.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_gluten_free">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/gluten_free.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_national_sanitation_foundation">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/nsf_international_logo.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_us_pharmacopeia">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/us_pharmacopeia.png')"></b-img>
              </b-form-checkbox>
              <b-form-checkbox class="my-1 mr-4" button button-variant="outline-success" v-model="certified_vegan">
                <b-img circle style="width:9em;" :src="require('../../assets/certifications/vegan.png')"></b-img>
              </b-form-checkbox>
            </div>
          </div>

          <div class="d-flex justify-content-end">
            <b-button type="submit" variant="primary">Submit</b-button>
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
@media only screen and (max-width: 1024px) {
    .my_component {
        width: 98%;
    }
}
</style>

<script>
export default {
  name: 'NewComponent',
  data: function () {
    return {
      edit_names_buffer: [
        {
          name_id: (Math.random() + 1).toString(36).substring(7),
          component_name: 'Placeholder',
          primary_name: false,
          botanical_name: false
        }
      ],
      component_type: null,
      component_options: [
        { value: 'powder', text: 'Powder' },
        { value: 'liquid', text: 'Liquid' },
        { value: 'container', text: 'Container' },
        { value: 'pouch', text: 'Pouch' },
        { value: 'shrink_band', text: 'Shrink Band' },
        { value: 'lid', text: 'Lid' },
        { value: 'label', text: 'Label' },
        { value: 'capsule', text: 'Capsule' },
        { value: 'misc', text: 'Miscellaneous' },
        { value: 'scoop', text: 'Scoop' },
        { value: 'desiccant', text: 'Desiccant' },
        { value: 'box', text: 'Box' },
        { value: 'carton', text: 'Carton' },
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
      certified_vegan: false
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
        name_id: (Math.random() + 1).toString(36).substring(7),
        component_name: '',
        primary_name: false,
        botanical_name: false
      }
      return newName
    }
  },
  watch: {
    component_type: function (val) {
      if (val === 'powder') {
        this.unit_type = 'kilograms'
      } else if (val === 'liquid') {
        this.unit_type = 'liters'
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
    },
    certified_usda_organic: function (val) {
      if (val === true) {
        this.certified_non_gmo = true
        this.certified_wildcrafted = false
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
    },
    certified_wildcrafted: function (val) {
      if (val === true) {
        this.certified_non_gmo = true
        this.certified_usda_organic = false
        this.certified_made_with_organic = false
      }
    }
  }
}
</script>
