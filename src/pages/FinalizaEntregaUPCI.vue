<template>
    <div v-if="entrega.estadoWorkflow" class="q-pa-md">
        <q-card class="my-card bg-teal-2">
            <q-card-section horizontal>
                <q-card-section>
                    <q-avatar color="white" text-color="cyan-8" icon="done" />
                </q-card-section>
                <q-card-section class="text-textoAzul">
                    <div class="text-h6"><b>Estado de la entrega actualizado.</b></div>
                    Gracias por usar Colabora
                </q-card-section>
            </q-card-section>      
            <q-card-section class="q-pt-none">
                <q-btn color="light-blue-10"
                    label="Volver a la bandeja de entregas"
                    @click="limpiaBandeja"
                />
            </q-card-section>
            <q-card-section>
                <q-separator class="bg-textoAzul" inset />
            </q-card-section>
        </q-card>
    </div>
    <div v-else class="q-pa-md">
        <div class="text-h6">
            Finalizando {{ entrega.aFinalizar.tipoEntrega }}
            <i>{{ entrega.aFinalizar.entrega.descripcion }}</i>
        </div>
        <q-form @submit="onSubmit" class="q-gutter-md">
            <q-input
                filled
                v-model="txtCumplimiento"
                label="Comentarios al cumplimiento de la entrega"
                hint="Analista describe criterios cumplidos, relaciona datos, actores, estado de parámetros y todo aquello que permitan que la entrega sea efectivo y aporte a la táctica."
                lazy-rules
                type="textarea"
                :rules="[
                    (val) =>
                    (val && val.length > 10) || 'Escriba por lo menos 10 caracteres',
                ]"
            />
            <div class="q-gutter-sm q-ma-md">
                <q-btn label="   Guardar   " type="submit" color="primary" />
                <q-btn label="   Cancelar  " color="secondary" @click="volver"/>
            </div>    
        </q-form>
    </div>
</template>
<script>
    import { computed, ref } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";

    export default {
    setup() {
        const router = useRouter();
        const store = useStore();
        const entrega = computed(() => store.state.entrega);
        const txtCumplimiento = ref(null);
        
        return {
            txtCumplimiento,
            entrega,
            limpiaBandeja: () => {                
                store.dispatch("entrega/limpiaEntregas");
                router.push("bandejaUPCI");
            },
            volver: () => {
                store.dispatch("entrega/limpiaEntregaAFinalizar");
                router.push("bandejaUPCI");
            },
            onSubmit: () => {
                store.dispatch("entrega/workflowUPCIDaVistoBueno", {
                    entrega_id: entrega.value.aFinalizar.entrega.id,
                    entrega_tipo: entrega.value.aFinalizar.tipoEntrega,
                    comentario_upci: txtCumplimiento.value,
                });
            },
        };
    },
};
</script>
