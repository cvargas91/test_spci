<template>
  <div v-if="datos">
    <apexchart type="heatmap" :options="chartOptions" :series="datos.series" />
  </div>
  <div v-else>Cargando...</div>
</template>
<script>
export default {
  props: {
    datos: Object,
  },
  setup(props) {
    return {
      chartOptions: {
        xaxis: {
          position: "top",
        },
        dataLabels: {
          enabled: false,
        },
        plotOptions: {
          heatmap: {
            colorScale: {
              ranges: [
                {
                  from: 0,
                  to: 1,
                  color: "#e0ffff",
                  name: "No impacta",
                },
                {
                  from: 1,
                  to: 2,
                  color: "#ea8c55",
                  name: "Impacta",
                },
              ],
            },
          },
        },
      },
    };
  },
};
</script>
