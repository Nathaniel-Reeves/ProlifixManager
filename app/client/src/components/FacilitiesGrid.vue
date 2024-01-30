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
    Facilities: Array
  },
  data () {
    return {
      cols: ['Building Name', 'Type'],
      facility_data: this.Facilities,
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    if (this.facility_data !== undefined) {
      this.facility_data.forEach(facility => {
        const row = [
          facility.building_name,
          facility.building_type
        ]
        this.rows.push(row)
      })
    }
  }
}
</script>
