<template>
  <div>
    <h3 id="Formulas">Formulas<b-button v-if="!edit_formulas" v-b-tooltip.hover title="Edit Product Formulas" @click="toggle_edit_formulas()" class="btn p-1 ml-2 btn-light" type="button"><b-icon icon="pencil-square" class="d-print-none"></b-icon></b-button></h3>

    <b-tabs content-class="mt-3" v-model="active_tab_index">
      <b-tab v-for="(f, index) in formulas" :key="'formula-id-' + index" :disabled="active_tab_index !== index && edit_formulas">
        <template #title>
          <strong>{{ f.formulation_version+'V' }}<b-badge variant="primary" pill class="ml-2" style="font-size:0.8em;" v-show="f.formula_id === defaultFormulaId">PF</b-badge></strong>
        </template>
        <b-card class="m-2">
          <b-card-title>
            Version {{ f.formulation_version }}
            <b-badge variant="primary" pill class="ml-2" style="font-size:0.8em;" v-show="f.formula_id === defaultFormulaId">Primary Formula</b-badge>
            <b-button v-show="f.formula_id !== defaultFormulaId && edit_formulas" variant="outline-primary" pill class="ml-2" style="font-size:0.8em;" @click="set_default_formula_id(f.formula_id)">Set as Primary</b-button>
          </b-card-title>
          <b-card-sub-title class="mb-3">{{ new Date(f.date_entered).toLocaleDateString() }} {{ new Date(f.date_entered).toLocaleTimeString() }}</b-card-sub-title>
          <b-card-text>
            <strong v-show="f.notes != null || f.notes?.length > 0">Notes:</strong>
            <b-form-textarea
              v-show="f.notes != null || f.notes?.length > 0"
              v-model="f.notes"
              placeholder="Notes..."
              rows="3"
              max-rows="6"
              id="new-formula-notes"
              class="mb-3"
              :disabled="!edit_formulas"
            ></b-form-textarea>
            <b-card-group deck class="mb-3">
              <b-card>
                <b-card-title>Powder Fill</b-card-title>
                <b-card-text>
                  <b-row>
                    <b-col><label :for="'max_grams_per_unit_'+f.formulation_version"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'max_grams_per_unit_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.max_grams_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'total_grams_per_unit_'+f.formulation_version"><strong>Target g per Product:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'total_grams_per_unit_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.total_grams_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'min_grams_per_unit_'+f.formulation_version"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'min_grams_per_unit_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.min_grams_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </b-card-text>
              </b-card>
              <b-card>
                <b-card-title>Liquid Fill</b-card-title>
                <b-card-text>
                  <b-row>
                    <b-col><label :for="'max_milliliters_per_unit_'+f.formulation_version"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'max_milliliters_per_unit_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.max_milliliters_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'total_milliliters_per_unit_'+f.formulation_version"><strong>Target ml per Product:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'total_milliliters_per_unit_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.total_milliliters_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'min_milliliters_per_unit_'+f.formulation_version"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'min_milliliters_per_unit_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.min_milliliters_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </b-card-text>
              </b-card>
              <b-card>
                <b-card-title>Capsule Fill</b-card-title>
                <b-card-text>
                  <b-row>
                    <b-col><label :for="'max_mg_per_capsule_'+f.formulation_version"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'max_mg_per_capsule_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.max_mg_per_capsule" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'total_mg_per_capsule_'+f.formulation_version"><strong>Target mg per Cap:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'total_mg_per_capsule_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.total_mg_per_capsule" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'min_mg_per_capsule_'+f.formulation_version"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'min_mg_per_capsule_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.min_mg_per_capsule" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <hr>
                  <b-row>
                    <b-col><label :for="'total_capsules_per_unit_'+f.formulation_version"><strong>Capsule Count:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'total_capsules_per_unit_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.total_capsules_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ct</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'capsule_size_'+f.formulation_version"><strong>Capsule Size:</strong></label></b-col>
                    <b-col><select :id="'capsule_size_'+f.formulation_version" disabled v-model="f.capsule_size" class="form-control form-control-md mb-3 hidedropdownarrow">
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="0">0</option>
                      <option value="00">00</option>
                    </select></b-col>
                  </b-row>
                  <b-row>
                    <b-col><label :for="'capsule_weight_'+f.formulation_version"><strong>Capsule Weight:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input :id="'capsule_weight_'+f.formulation_version" type="number" class="form-control" disabled v-model="f.capsule_weight" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </b-card-text>
              </b-card>
            </b-card-group>

            <b-table-lite :items="f['formula_detail']" :fields="fields" striped bordered sticky-header foot-clone head-variant="light" style="min-height: 600px;">
              <template #cell(ingredients_detail)="ingredients_detail">
                <div v-for="(ing, index) in ingredients_detail.value" :key="ing.component_id+'-ingredient'">
                  <b-row style="height:80px;" align-v="center">
                    <b-col cols="1">
                      <b-badge :id="f.formulation_version+'-'+ingredients_detail.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" v-bind:variant="(ing.priority === 1 ? 'primary' : 'light')" pill class="ml-2">{{ ing.priority }}</b-badge>
                      <b-tooltip :target="f.formulation_version+'-'+ingredients_detail.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" triggers="hover">Priority Level: {{ ing.priority }}</b-tooltip>
                    </b-col>
                    <b-col cols="3"><b-link :to="'/catalogue/components/'+ing.component_id" target="_blank">{{ ing.component_name }}</b-link></b-col>
                    <b-col><CertBadge :data="ing"></CertBadge></b-col>
                  </b-row>
                  <hr v-show="index < ingredients_detail.value.length-1">
                </div>
              </template>
              <template #foot(ingredients_detail)=""></template>
              <template #cell(brands)="brands">
                <div v-if="!edit_formulas">
                  <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                    <div class="py-3" style="height:80px;">
                      <b-badge :id="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill class="mr-2">{{ brand.priority }}</b-badge>
                      <b-tooltip :target="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                      <span :id="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-name'">{{ brand.organization_initial }}</span>
                      <b-tooltip :target="f.formulation_version+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-name'" triggers="hover">{{ brand.organization_name }}</b-tooltip>
                    </div>
                    <hr v-show="index < brands.value.length-1">
                  </div>
                </div>
                <div v-else>
                  <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                    <b-row class="py-3" style="height:80px;">
                      <b-col cols="1">
                        <b-badge :id="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill class="mr-2">{{ brand.priority }}</b-badge>
                        <b-tooltip :target="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                      </b-col>
                      <b-col>
                        <ChooseOrg @org="(o) => select_brand(o, brands.item.brands, index)" :organizations="organization_options" :selected="brand.organization_id === 0 ? null : brand"></ChooseOrg>
                      </b-col>
                    </b-row>
                    <hr v-show="index < brands.value.length">
                  </div>
                  <b-button variant="outline-info" @click="add_brand(brands.item.brands)">Add Brand</b-button>
                </div>
              </template>
              <template #foot(brands)=""></template>
              <template #cell(percent)="percent">
                <strong style="font-size: 1.5em;">{{ percent.value }}%</strong>
              </template>
              <template #foot(percent)="">
                <span :class="calc_total(f['formula_detail']) !== 100 ? 'text-danger':''">= {{ calc_total(f['formula_detail']) }}%</span>
              </template>
              <template #cell(specific_brand_required)="specific_brand_required">
                <span v-if="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
              </template>
              <template #foot(specific_brand_required)=""></template>
              <template #cell(specific_ingredient_required)="specific_ingredient_required">
                <div v-if="!edit_formulas">
                  <span v-if="specific_ingredient_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</span>
                  <span v-else class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</span>
                </div>
                <div v-else>
                  <b-button @click="specific_ingredient_required.item.specific_ingredient_required = false" v-show="specific_ingredient_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                  <b-button @click="specific_ingredient_required.item.specific_ingredient_required = true" v-show="!specific_ingredient_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
                </div>
              </template>
              <template #foot(specific_ingredient_required)=""></template>
              <template #cell(notes)="notes">
                <div v-if="!edit_formulas">{{ notes.value }}</div>
                <b-form-textarea
                  v-else
                  v-model="notes.item.notes"
                  placeholder="Notes..."
                  rows="3"
                  max-rows="6"
                  :id="notes.item.formula_ingredient_id+'-notes'"
                ></b-form-textarea>
              </template>
              <template #foot(notes)=""></template>
            </b-table-lite>
          </b-card-text>
          <b-button v-show="edit_formulas" class="mr-2" variant="outline-success" @click="update_formula(f, index)">Save</b-button>
          <b-button variant="outline-danger" v-show="edit_formulas" @click="toggle_edit_formulas()">Cancel</b-button>
        </b-card>
      </b-tab>

      <b-tab title="New Formula" :disabled="edit_formulas && active_tab_index !== numVersions">
        <b-card class="m-2">
          <b-card-title>New Formula Version {{ numVersions + 1 }}</b-card-title>
          <select id="new_version_selector" class="form-control form-control-lg mb-3" v-model="new_version_select"  @change="set_formula_buffer()" :disabled="disable_version_select">
            <option v-for="option in versions" :key="option.value" :value="option.value">{{ option.text }}</option>
          </select>
          <div v-if="disable_version_select">
            <strong>Notes:</strong>
            <b-form-textarea
              v-model="new_formula_buffer.notes"
              placeholder="Notes..."
              rows="3"
              max-rows="6"
              id="new-formula-notes"
              class="mb-3"
            ></b-form-textarea>
            <b-card-group deck class="mb-3">
              <b-card>
                <b-card-title>Powder Fill</b-card-title>
                <b-card-text>
                  <b-row>
                    <b-col><label for="max_grams_per_unit"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="max_grams_per_unit" type="number" class="form-control" v-model="new_formula_buffer.max_grams_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="total_grams_per_unit"><strong>Target g per Product:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="total_grams_per_unit" type="number" class="form-control" v-model="new_formula_buffer.total_grams_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="min_grams_per_unit"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="min_grams_per_unit" type="number" class="form-control" v-model="new_formula_buffer.min_grams_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">g</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </b-card-text>
              </b-card>
              <b-card>
                <b-card-title>Liquid Fill</b-card-title>
                <b-card-text>
                  <b-row>
                    <b-col><label for="max_milliliters_per_unit"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="max_milliliters_per_unit" type="number" class="form-control" v-model="new_formula_buffer.max_milliliters_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="total_milliliters_per_unit"><strong>Target ml per Product:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="total_milliliters_per_unit" type="number" class="form-control" v-model="new_formula_buffer.total_milliliters_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="min_milliliters_per_unit"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="min_milliliters_per_unit" type="number" class="form-control" v-model="new_formula_buffer.min_milliliters_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ml</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </b-card-text>
              </b-card>
              <b-card>
                <b-card-title>Capsule Fill</b-card-title>
                <b-card-text>
                  <b-row>
                    <b-col><label for="max_mg_per_capsule"><strong>Tolerance Max:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="max_mg_per_capsule" type="number" class="form-control" v-model="new_formula_buffer.max_mg_per_capsule" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="total_mg_per_capsule"><strong>Target mg per Cap:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="total_mg_per_capsule" type="number" class="form-control" v-model="new_formula_buffer.total_mg_per_capsule" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="min_mg_per_capsule"><strong>Tolerance Min:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="min_mg_per_capsule" type="number" class="form-control" v-model="new_formula_buffer.min_mg_per_capsule" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <hr>
                  <b-row>
                    <b-col><label for="total_capsules_per_unit"><strong>Capsule Count:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="total_capsules_per_unit" type="number" class="form-control" v-model="new_formula_buffer.total_capsules_per_unit" required>
                        <div class="input-group-append">
                          <span class="input-group-text">ct</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="capsule_size"><strong>Capsule Size:</strong></label></b-col>
                    <b-col><select id="capsule_size" v-model="new_formula_buffer.capsule_size" class="form-control form-control-md mb-3">
                      <option value="1">1</option>
                      <option value="2">2</option>
                      <option value="0">0</option>
                      <option value="00">00</option>
                    </select></b-col>
                  </b-row>
                  <b-row>
                    <b-col><label for="capsule_weight"><strong>Capsule Weight:</strong></label></b-col>
                    <b-col>
                      <div class="input-group mb-2">
                        <input id="capsule_weight" type="number" class="form-control" v-model="new_formula_buffer.capsule_weight" required>
                        <div class="input-group-append">
                          <span class="input-group-text">mg</span>
                        </div>
                      </div>
                    </b-col>
                  </b-row>
                </b-card-text>
              </b-card>
            </b-card-group>
            <b-table-lite :items="new_formula_buffer.formula_detail" :fields="fields" striped bordered foot-clone sticky-header head-variant="light" style="max-height: 600px;">
              <template #cell(ingredients_detail)="ingredients">
                <div v-for="(ing, index) in ingredients.value" :key="ing.component_id+'-ingredient'">
                  <b-row style="height:80px;">
                    <b-col cols="1">
                      <b-badge :id="(numVersions+1)+'-'+ingredients.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" v-bind:variant="(ing.priority === 1 ? 'primary' : 'light')" pill class="mr-1 mt-4">{{ ing.priority }}</b-badge>
                      <b-tooltip :target="(numVersions+1)+'-'+ingredients.item.formula_ingredient_id+'-'+ing.component_id+'-ingredient-priority'" triggers="hover">Priority Level: {{ ing.priority }}</b-tooltip>
                    </b-col>
                    <b-col><ChooseIngredient class="py-3" @ing="(i) => select_ing(i, ingredients.item.ingredients_detail, index)" :ingredients="ingredient_options" :selected="ing.component_id === 0 ? null : ing"></ChooseIngredient></b-col>
                  </b-row>
                  <hr v-show="index < ingredients.value.length">
                </div>
                <b-button variant="outline-info" @click="add_ing(ingredients.item.ingredients_detail)">Add Ingredient</b-button>
              </template>
              <template #foot(ingredients_detail)=""></template>
              <template #cell(brands)="brands">
                <div v-for="(brand, index) in brands.value" :key="brand.organization_id+'-org'">
                  <b-row class="py-3" style="height:80px;">
                    <b-col cols="1">
                      <b-badge :id="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" v-bind:variant="(brand.priority === 1 ? 'primary' : 'light')" pill class="mr-2">{{ brand.priority }}</b-badge>
                      <b-tooltip :target="(numVersions+1)+'-'+brands.item.formula_ingredient_id+'-'+brand.organization_id+'-org-priority'" triggers="hover">Priority Level: {{ brand.priority }}</b-tooltip>
                    </b-col>
                    <b-col>
                      <ChooseOrg @org="(o) => select_brand(o, brands.item.brands, index)" :organizations="organization_options" :selected="brand.organization_id === 0 ? null : brand"></ChooseOrg>
                    </b-col>
                  </b-row>
                  <hr v-show="index < brands.value.length">
                </div>
                <b-button variant="outline-info" @click="add_brand(brands.item.brands)">Add Brand</b-button>
              </template>
              <template #foot(brands)=""></template>
              <template #cell(percent)="percent">
                <div class="input-group mb-2" style="font-size: 1.5em; width: 80px;">
                  <strong><input :id="percent.item.formula_ingredient_id+'-percent'" type="number" class="form-control" v-model="percent.item.percent" required min="0" max="100"></strong>
                </div>
              </template>
              <template #foot(percent)="">
                <span :class="calc_total(new_formula_buffer.formula_detail) !== 100 ? 'text-danger':''">= {{ calc_total(new_formula_buffer.formula_detail) }}%</span>
              </template>
              <template #cell(specific_brand_required)="specific_brand_required">
                <b-button @click="specific_brand_required.item.specific_brand_required = false" v-show="specific_brand_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="specific_brand_required.item.specific_brand_required = true" v-show="!specific_brand_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
              </template>
              <template #foot(specific_brand_required)=""></template>
              <template #cell(specific_ingredient_required)="specific_ingredient_required">
                <b-button @click="specific_ingredient_required.item.specific_ingredient_required = false" v-show="specific_ingredient_required.value" class="badge badge-success badge-pill" style="font-size: 1.5em;">Yes</b-button>
                <b-button @click="specific_ingredient_required.item.specific_ingredient_required = true" v-show="!specific_ingredient_required.value" class="badge badge-warning badge-pill" style="font-size: 1.5em;">No</b-button>
              </template>
              <template #foot(specific_ingredient_required)=""></template>
              <template #cell(notes)="notes">
                <b-form-textarea
                  v-model="notes.item.notes"
                  placeholder="Notes..."
                  rows="3"
                  max-rows="6"
                  :id="notes.item.formula_ingredient_id+'-notes'"
                ></b-form-textarea>
              </template>
              <template #foot(notes)=""></template>
            </b-table-lite>
          </div>
          <b-button :disabled="!disable_version_select" class="mr-2" variant="outline-success" @click="save_new_formula()">Save</b-button>
          <b-button :disabled="!disable_version_select" class="mr-2" variant="outline-info" @click="add_row()">Add Row</b-button>
          <b-button :disabled="!disable_version_select" variant="outline-danger" @click="cancel_new_formula()">Cancel</b-button>
        </b-card>
      </b-tab>

      <template #empty>
        <div class="text-center text-muted">
          There are not formulas yet.<br>
          Create a new formula using the <b>New Formula</b> button above.
        </div>
      </template>
    </b-tabs>
  </div>
</template>

<style scoped>
.hidedropdownarrow {
  -webkit-appearance: none;
  -moz-appearance: none;
  text-indent: 1px;
  text-overflow: '';
}

.card {
  box-shadow: 0 2px 2px rgba(0,0,0,.2);
}

.custom-row {
  border-bottom-width: thick !important;
  border-top-width: thick !important;
}
</style>

<script>
import CertBadge from '../../../components/CertBadge.vue'
import ChooseIngredient from '../../../components/ChooseIngredient.vue'
import ChooseOrg from '../../../components/ChooseOrg.vue'
import { cloneDeep, tap } from 'lodash'

export default {
  name: 'ProductFormula',
  components: {
    CertBadge,
    ChooseIngredient,
    ChooseOrg
  },
  props: {
    formulas: {
      type: Array,
      required: true
    },
    defaultFormulaId: {
      type: Number,
      required: true
    },
    numVersions: {
      type: Number,
      required: true
    },
    productId: {
      type: String,
      required: true
    }
  },
  emits: ['update:formulas', 'update:defaultFormulaId', 'update:numVersions'],
  data: function () {
    return {
      edit_formulas: false,
      new_version_select: '',
      disable_version_select: false,
      new_formula_buffer: {},
      fields: [
        { label: 'Ingredient', key: 'ingredients_detail', tdClass: 'custom-row' },
        { label: 'Brands', key: 'brands', tdClass: 'custom-row' },
        { label: '%', key: 'percent', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Brand Specific', key: 'specific_brand_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Cert Specific', key: 'specific_ingredient_required', tdClass: ['align-middle', 'custom-row'], class: 'text-center' },
        { label: 'Notes', key: 'notes', tdClass: ['align-middle', 'custom-row'] }
      ],
      versions: [],
      organization_options: [],
      ingredient_options: [],
      new_formula_id: ('t-' + Math.floor(Math.random() * 100000)),
      new_formula_ingredient_id_index: 0,
      active_tab_index: 0
    }
  },
  methods: {
    set_default_formula_id: function (version) {
      this.$emit('update:defaultFormulaId', version)
    },
    update_formula: function (formula, index) {
      this.$emit('update:formulas', tap(cloneDeep(this.formulas), v => v.splice(index, 1, formula)))
      this.toggle_edit_formulas()
    },
    save_new_formula: function () {
      this.$emit('update:numVersions', this.numVersions + 1)
      this.$emit('update:formulas', tap(cloneDeep(this.formulas), v => v.push(cloneDeep(this.new_formula_buffer))))
      this.cancel_new_formula()
      this.toggle_edit_formulas()
      this.$nextTick(() => {
        this.versions = []
        this.build_formula_versions()
      })
    },
    toggle_edit_formulas: function () {
      this.edit_formulas = !this.edit_formulas
      this.$emit('editFormulas', this.edit_formulas)
    },
    cancel_new_formula: function () {
      this.disable_version_select = false
      this.new_version_select = ''
      this.new_formula_buffer = {}
      this.$nextTick(() => {
        this.toggle_edit_formulas()
      })
    },
    calc_total: function (formulaDetail) {
      let total = 0
      for (const f in formulaDetail) {
        total += formulaDetail[f].percent
      }
      return Math.round(total * 100) / 100
    },
    add_brand: function (brands) {
      const brand = {
        organization_id: 0,
        priority: brands.length + 1
      }
      brands.push(brand)
    },
    select_brand: function (org, brands, index) {
      const priority = brands[index].priority
      if (org != null) {
        brands[index] = org
        brands[index].priority = priority
      }
    },
    add_ing: function (ingredientsDetail) {
      const brand = {
        component_id: 0,
        priority: ingredientsDetail.length + 1
      }
      ingredientsDetail.push(brand)
    },
    select_ing: function (ing, ingredients, index) {
      const priority = ingredients[index].priority
      if (ing != null) {
        ingredients[index] = ing
        ingredients[index].priority = priority
      }
    },
    add_row: function () {
      const row = {
        brands: [{
          organization_id: 0,
          priority: 1
        }],
        formula_id: this.new_formula_id,
        formula_ingredient_id: this.new_formula_id + '-' + this.new_formula_ingredient_id_index,
        grams_per_unit: null,
        ingredients_detail: [{
          component_id: 0,
          priority: 1
        }],
        mg_per_capsule: null,
        ml_per_unit: null,
        notes: null,
        percent: 0,
        specific_brand_required: false,
        specific_ingredient_required: false
      }
      this.new_formula_ingredient_id_index++
      this.new_formula_buffer.formula_detail.push(row)
    },
    set_formula_buffer: function () {
      if (this.new_version_select === 'NEW') {
        this.new_formula_buffer = {
          formulation_version: this.numVersions + 1,
          formula_id: 't-' + this.new_formula_id,
          date_entered: new Date(),
          notes: '',
          min_grams_per_unit: 0,
          total_grams_per_unit: 0,
          max_grams_per_unit: 0,
          min_milliliters_per_unit: 0,
          total_milliliters_per_unit: 0,
          max_milliliters_per_unit: 0,
          min_mg_per_capsule: 0,
          total_mg_per_capsule: 0,
          max_mg_per_capsule: 0,
          total_capsules_per_unit: 0,
          capsule_size: '',
          capsule_weight: 0,
          formula_detail: []
        }
        this.disable_version_select = true
      } else {
        this.new_formula_buffer = structuredClone(this.formulas.find(f => f.formulation_version === this.new_version_select))
        this.new_formula_buffer.formulation_version = this.numVersions + 1
        this.new_formula_buffer.formula_id = this.new_formula_id
        this.new_formula_buffer.date_entered = new Date()
        this.disable_version_select = true
      }
    },
    build_formula_versions: function () {
      for (const f in this.formulas) {
        this.versions.push({ value: this.formulas[f].formulation_version, text: 'Copy V' + this.formulas[f].formulation_version + (this.formulas[f].formula_id === this.defaultFormulaId ? ' (PRIMARY)' : '') })
      }
      this.versions.push({ value: 'NEW', text: 'New Formula' })
    },
    get_component_primary_name: function (component) {
      if (component.component_name !== undefined) {
        return component.component_name
      }
      if (component.Component_Names !== undefined && component.Component_Names.length > 0) {
        for (let i = 0; i < component.Component_Names.length; i++) {
          if (component.Component_Names[i].primary_name) {
            component.component_name = component.Component_Names[i].component_name
            return component.Component_Names[i].component_name
          }
        }
      }
      return 'No Name'
    },
    get_organization_primary_name: function (organization) {
      if (organization.organization_name !== undefined) {
        return organization.organization_name
      }
      if (organization.Organization_Names !== undefined && organization.Organization_Names.length > 0) {
        for (let i = 0; i < organization.Organization_Names.length; i++) {
          if (organization.Organization_Names[i].primary_name) {
            organization.organization_name = organization.Organization_Names[i].organization_name
            organization.organization_initial = organization.Organization_Names[i].organization_initial
            return organization.Organization_Names[i].organization_name
          }
        }
      }
      return 'No Name'
    },
    get_organizations: function () {
      const fetchRequest = window.origin + '/api/v1/organizations?org-type=supplier'
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
            const orgs = Object.values(data.data[0])
            this.organization_options = orgs.sort((a, b) => (this.get_organization_primary_name(a) > this.get_organization_primary_name(b) ? 1 : -1))
            // eslint-disable-next-line
            console.log(this.organization_options)
            if (this.organization_options.doc === null) {
              this.organization_options.doc = {}
            }
          })
        } else if (response.status === 404) {
          this.$router.push({ path: '/404' })
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
    },
    get_ingredients: function () {
      const fetchRequest = window.origin + '/api/v1/catalogue/components?type=powder'
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
            const ings = Object.values(data.data[0])
            for (const i in ings) {
              this.get_component_primary_name(ings[i])
            }
            this.ingredient_options = ings.sort((a, b) => (a.component_name > b.component_name ? 1 : -1))
            // eslint-disable-next-line
            console.log(this.ingredient_options)
          })
        } else if (response.status === 404) {
          this.$router.push({ path: '/404' })
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
  watch: {
    new_version_select: function () {
      this.toggle_edit_formulas()
    }
  },
  created: function () {
    this.build_formula_versions()
    this.get_organizations()
    this.get_ingredients()
  }
}
</script>
