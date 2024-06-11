<template>
  <b-card class="m-2">
    <b-card-title>Version {{ formula.formulation_version }}  <b-badge variant="primary" pill class="ml-2" style="font-size:0.8em;" v-show="primary">Primary Formula</b-badge></b-card-title>
    <b-card-sub-title class="mb-3">{{ new Date(formula.date_entered).toLocaleDateString() }} {{ new Date(formula.date_entered).toLocaleTimeString() }}</b-card-sub-title>
    <b-card-text>
      <p v-show="formula.notes != null || formula.notes?.length > 0"><strong>Notes:</strong><br>{{ formula.notes }}</p>
      <b-card-group deck class="mb-3">
        <b-card>
          <b-card-title>Powder Fill</b-card-title>
          <b-card-text>
            <b-row>
              <b-col><strong>Tolerance Max:</strong></b-col>
              <b-col>{{ formula.min_grams_per_unit }}g</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Target g per Product:</strong></b-col>
              <b-col>{{ formula.total_grams_per_unit }}g</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Tolerance Min:</strong></b-col>
              <b-col>{{ formula.max_grams_per_unit }}g</b-col>
            </b-row>
          </b-card-text>
        </b-card>
        <b-card>
          <b-card-title>Liquid Fill</b-card-title>
          <b-card-text>
            <b-row>
              <b-col><strong>Tolerance Max:</strong></b-col>
              <b-col>{{ formula.min_milliliters_per_unit }}ml</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Target ml per Product:</strong></b-col>
              <b-col>{{ formula.total_milliliters_per_unit }}ml</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Tolerance Min:</strong></b-col>
              <b-col>{{ formula.max_milliliters_per_unit }}ml</b-col>
            </b-row>
          </b-card-text>
        </b-card>
        <b-card>
          <b-card-title>Capsule Fill</b-card-title>
          <b-card-text>
            <b-row>
              <b-col><strong>Tolerance Max:</strong></b-col>
              <b-col>{{ formula.min_mg_per_capsule }}mg</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Target mg per Cap:</strong></b-col>
              <b-col>{{ formula.total_mg_per_capsule }}mg</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Tolerance Min:</strong></b-col>
              <b-col>{{ formula.max_mg_per_capsule }}mg</b-col>
            </b-row>
            <hr>
            <b-row>
              <b-col><strong>Tolerance Max:</strong></b-col>
              <b-col>{{ (formula.min_mg_per_capsule + formula.capsule_weight) * 10 / 1000 }}g</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Target per 10 Caps:</strong></b-col>
              <b-col>{{ (formula.total_mg_per_capsule + formula.capsule_weight) * 10 / 1000 }}g</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Tolerance Min:</strong></b-col>
              <b-col>{{ (formula.max_mg_per_capsule + formula.capsule_weight) * 10 / 1000 }}g</b-col>
            </b-row>
            <hr>
            <b-row>
              <b-col><strong>Capsule Count:</strong></b-col>
              <b-col>{{ formula.total_capsules_per_unit }}ct</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Capsule Size:</strong></b-col>
              <b-col>{{ formula.capsule_size }}</b-col>
            </b-row>
            <b-row>
              <b-col><strong>Capsule Weight:</strong></b-col>
              <b-col>{{ formula.capsule_weight }}mg</b-col>
            </b-row>
          </b-card-text>
        </b-card>
      </b-card-group>

      <b-table-lite :items="formula['formula_detail']" :fields="fields" stacked="md" striped bordered>
        <template #cell(ingredients_detail)="ingredients">
          <div v-for="(ing, index) in ingredients.value" :key="ing.component_id+'-ingredient'">
            <b-row style="height:80px;">
              <b-col cols="1">
                <b-badge :id="ing.component_id+'-ingredient-priority'" v-bind:variant="(ing.priority === 1 ? 'primary' : 'light')" pill class="ml-2 mt-3">{{ ing.priority }}</b-badge>
                <b-tooltip :target="ing.component_id+'-ingredient-priority'" triggers="hover">Priority Level: {{ ing.priority }}</b-tooltip>
              </b-col>
              <b-col cols="3"><b-link :to="'/catalogue/components/'+ing.component_id" target="_blank"><p class="py-3">{{ ing.component_name }}</p></b-link></b-col>
              <b-col><CertBadge :data="ing"></CertBadge></b-col>
            </b-row>
            <hr v-show="index < ingredients.value.length-1">
          </div>
        </template>
        <template #cell(brands)="brands">
          <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
            <p class="py-3" style="height:80px;">
              <b-badge :id="brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill class="mr-2">{{ brand.priority }}</b-badge>
              <b-tooltip :target="brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
              <span :id="brand.organization_id+'-org-name'">{{ brand.organization_initial }}</span>
              <b-tooltip :target="brand.organization_id+'-org-name'" triggers="hover">{{ brand.organization_name }}</b-tooltip>
            </p>
            <hr v-show="index < brands.value.length-1">
          </div>
        </template>
        <template #cell(percent)="percent">
          <strong style="font-size: 1.5em;">{{ percent.value }}%</strong>
        </template>
        <template #cell(specific_brand_required)="specific_brand_required">
          <span v-if="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
          <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
        </template>
        <template #cell(specific_ingredient_required)="specific_ingredient_required">
          <span v-if="specific_ingredient_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
          <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
        </template>
        <template #cell(notes)="notes">
          {{ notes.value }}
        </template>
      </b-table-lite>
    </b-card-text>
  </b-card>
</template>

<style scoped>
.card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}
</style>

<style>
.custom-row {
  border-bottom-width: thick !important;
  border-top-width: thick !important;
}
</style>

<script>
import CertBadge from '../../components/CertBadge.vue'

export default {
  name: 'ProductFormula',
  components: {
    CertBadge
  },
  props: {
    formula: {
      type: Object,
      required: true
    },
    edit: {
      type: Boolean,
      required: true,
      default: false
    },
    primary: {
      type: Boolean,
      required: true,
      default: false
    }
  },
  data: function () {
    return {
      fields: [
        { label: 'Ingredient', key: 'ingredients_detail', tdClass: 'custom-row' },
        { label: 'Brands', key: 'brands', tdClass: 'custom-row' },
        { label: '%', key: 'percent', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Brand Specific', key: 'specific_brand_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Cert Specific', key: 'specific_ingredient_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Notes', key: 'notes', tdClass: 'custom-row' }
      ]
    }
  },
  methods: {
  }
}
</script>
