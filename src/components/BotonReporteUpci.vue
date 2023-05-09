<template>
    <q-btn
        v-if="seRenderea"
        :label="etiqueta"
        color="light-blue-10"
        @click="accionBoton"
    />
</template>
<script>
    import { ref, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";

    export default defineComponent({
        props: {
        usuario: Object,
        entrega: Object,
        tipoEntrega: String,
        },
    
        setup(props) {
            const store = useStore();
            const seRenderea = ref(true);
            const etiqueta = ref("");
            const accion = ref("");
            const router = useRouter();

            if (props.entrega.estado == "Finalizado" && props.usuario.perfil.esAnalistaUPCI) {
                etiqueta.value = "Generar Reporte";
                //accion.value = "UPCIFinaliza";
            }

            return {
                etiqueta,
                seRenderea,
                accionBoton: () => {
                    router.push("reporteUpci");
                },
            };
        }
    })
</script>
