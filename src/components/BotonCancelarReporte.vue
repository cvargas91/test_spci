<template>
    <PopupCancelarNuevoReporte
        :mostrar="mostrarPopupCancelar"
        @update:mostrar="mostrarPopupCancelar = $event"
        @respuestaPopup="handlerPopupCancelar"
    />
    <q-btn
        class="q-ml-sm"
        color="btnCancelar"
        label="   Cancelar   "
        @click="cancelarReporte"
    />
    
</template>
<script>
    import { ref,toRef,watch, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";
    import PopupCancelarNuevoReporte from "src/components/PopupCancelarNuevoReporte.vue";    

    export default defineComponent({
    components: { 
        PopupCancelarNuevoReporte 
    },
    props: {
        opcion: String,
    },
    emits:["guardarAvance"],
    setup(props, { emit }) {
        const store = useStore();
        const router = useRouter();
        const mostrar = ref("");
        const mostrarPopupCancelar = ref(false);
        const reporte = computed(() => store.state.reporte);
        const handlerPopupCancelar = (respuesta) => {
                mostrarPopupCancelar.value = false;
                if (respuesta == "guarda") {
                    emit("guardarAvance");
                } else if (respuesta == "sale") {
                    store.dispatch("reporte/limpiaReporteFunciones");
                    store.dispatch("reporte/limpiaReporteHitos");
                    
                    store.dispatch("reporte/reqReportesBorradores");
                    store.dispatch("reporte/reqReportesUpci");
                    
                    router.push("panelReportesUpci");
                } else {
                // se hace nada
                }
        };

        return {
            reporte,
            handlerPopupCancelar,
            cancelarReporte: () => {
                mostrarPopupCancelar.value = true;
                //store.dispatch("accion/limpiaAccionAReportar");
                //store.dispatch("reporte/limpiaReporteFunciones");
                //store.dispatch("reporte/limpiaReporteHitos");
                //router.push("panelReportesUpci");
            },
            mostrar,
            mostrarPopupCancelar,
        };
    },
})
</script>