<template>
    aca los reportes en estado finalizado
    {{reportesFinalizados}}
</template>

<script>
import { ref, toRef, computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { route } from "quasar/wrappers";

export default defineComponent({
    props: {
        reportesFinalizados: Array,
    },
    setup(props) {
        const store = useStore();
        const router = useRouter();
        
        onMounted(() => {
            //store.dispatch("reporte/reqReportesUpci");reqVerificadorPorIndicador
        });
        
        return {
            reportesFinalizados: toRef(props, "reportesFinalizados"),
        };
    }
    
});
</script>