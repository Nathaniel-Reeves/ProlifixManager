<template>
    <Grid :cols="cols" :rows="rows" :pagination="{'limit':5}" :sort="true"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'FacilitiesGrid',
  components: {
    Grid
  },
  props: {
    facilities: Object
  },
  data () {
    return {
      cols: ['Building Name', 'Type'],
      facility_data: Object.values(this.facilities),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    this.facility_data.forEach(facility => {
      const row = [
        facility.building_name,
        facility.building_type
      ]
      this.rows.push(row)
    })
  }
}
</script>
