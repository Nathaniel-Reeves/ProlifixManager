<template>
    <div class="gridchart">
        <h1>This is a Chart Page</h1>
        <GridChart/>
    </div>
</template>
<script>
import GridChart from '../components/GridChart.vue'

export default {
  name: 'FirstGridChart',
  components: { GridChart }
}
</script>
