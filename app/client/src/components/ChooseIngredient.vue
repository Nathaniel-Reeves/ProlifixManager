<template>
  <div>
    <b-row align-v="center">
      <b-col style="max-width: 260px;">
        <v-select
          :options="ingredients"
          label="component_name"
          v-model="selected_ingredient"
          :loading="!ingredients_loaded"
          :clearable="selected_ingredient != null"
          :placeholder="!ingredients_loaded ? 'Loading...':'Choose...'"
          style="width: 250px;"
          aria-describedby="select_ingredient-live-feedback"
          :class="(selected_ingredient !== null ? '' : 'is-invalid')"
        >
          <template #option="{ component_id, component_name, certified_fda, certified_gluten_free, certified_gmp, certified_halal, certified_kosher, certified_made_with_organic, certified_national_sanitation_foundation, certified_non_gmo, certified_us_pharmacopeia, certified_usda_organic, certified_vegan, certified_wildcrafted }">
            <div style="display:flex; flex-direction: row; align-items: center; min-height: 60px;">
              <b-button v-on:click.stop class="mr-2" variant="light" :to="'/catalogue/components/'+component_id" target="_blank"><b-icon icon="box"></b-icon></b-button>
              <div style="min-width: 200px;">{{ component_name }}</div>
              <CertBadge :data="{
                'certified_fda': certified_fda,
                'certified_gluten_free': certified_gluten_free,
                'certified_gmp': certified_gmp,
                'certified_halal': certified_halal,
                'certified_kosher': certified_kosher,
                'certified_made_with_organic': certified_made_with_organic,
                'certified_national_sanitation_foundation': certified_national_sanitation_foundation,
                'certified_non_gmo': certified_non_gmo,
                'certified_us_pharmacopeia': certified_us_pharmacopeia,
                'certified_usda_organic': certified_usda_organic,
                'certified_vegan': certified_vegan,
                'certified_wildcrafted': certified_wildcrafted
              }"></CertBadge>
            </div>
          </template>
        </v-select>
        <div id="select_ingredient-live-feedback" class="invalid-feedback">This is a required field.</div>
      </b-col>
      <b-col style="max-width: 300px;">
        <CertBadge :data="selected_ingredient"></CertBadge>
      </b-col>
    </b-row>
  </div>
</template>

<style>
.vs__dropdown-menu {
  width: 600px;
  max-height: 300px;
  overflow-y: auto;
}
</style>

<script>
import CertBadge from './CertBadge.vue'
import vSelect from 'vue-select'
// import { createPopper } from '@popperjs/core'

export default {
  name: 'ChooseIngredient',
  components: {
    CertBadge,
    vSelect
  },
  props: [
    'ingredients',
    'selected'
  ],
  data: function () {
    return {
      selected_ingredient: null
    }
  },
  watch: {
    selected_ingredient: function (val) {
      this.$emit('ing', val)
    }
  },
  computed: {
    ingredients_loaded: function () {
      return this.ingredients.length > 0
    },
    ing_array: function () {
      if (Array.isArray(this.ingredients) && this.ingredients.length > 0) {
        return this.ingredients
      }
      return []
    }
  },
  created: function () {
    this.selected_ingredient = this.selected != null ? this.selected : null
  }
}
</script>
