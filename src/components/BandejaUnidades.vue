<template>    
    <div class="q-gutter-y-md">        
        <div class="text-subtitle1 text-textoAzul" v-if="seRenderea">
                <b>Unidad: {{ actor.nombre }}</b>
        </div>
        <div class="q-gutter-y-md">
            <q-card>
                <q-card-section>
                    <q-select
                        filled                
                        :options="actores"
                        label="Unidades"
                        color="teal"
                        clearable
                        options-selected-class="text-deep-orange"                
                        option-label="sigla"                    
                        :model-value="actor"
                        @update:model-value="cambio"
                    >
                    <!--:model-value="actor"
                    @update:model-value="cambio"-->
                        <template v-slot:option="scope">
                            <q-item v-bind="scope.itemProps">
                            
                                <q-item-section>
                                    <q-item-label>{{ scope.opt.sigla }}</q-item-label>
                                    <q-item-label caption>{{ scope.opt.nombre }}</q-item-label>
                                </q-item-section>
    
                            </q-item>
                        </template>                
                    </q-select>
                </q-card-section>
                <q-card-section v-if="seRenderea" v-model="actor">
                    <!--<q-card >-->
                        <TablaAccionesUnidad 
                            :id_responsable="actor.id"
                            :acciones="accion.acciones"
                            :origen="origen"
                            :reportes="reportes"
                        />
                    <!--</q-card>-->
                </q-card-section>      
            </q-card>                                
        </div>
    </div>
    
</template>
<script>
import { ref, toRef, computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";
import TablaAccionesUnidad from "src/components/TablaAccionesUnidad.vue";


export default defineComponent({
    components:{
        TablaAccionesUnidad,
    },
    props:{
        origen: String,
        reportes: Array,
    },
    setup(props) {
        const store = useStore();
        const actores = computed(() => store.state.actor.actores);
        const accion = computed(() => store.state.accion);
        const actorInicial = "Seleccione una Unidad";
        const actor = ref(null);
        const detalleActor = ref("");
        const seRenderea = ref(null);
        const id_responsable = ref("");
        const model = ref(null);        
        
        const cambio = (value, event) => {
            if(value){                
                seRenderea.value = false;
                store.dispatch("accion/limpiaAcciones");
                if(props.origen === "POA"){
                    store.dispatch("accion/reqAccionesPorRolResponsable", value.id);
                }else{
                    store.dispatch("accion/reqAccionesPorRolResponsablePMI", value.id);
                }
                actor.value = value;
                id_responsable.value = value.id;
                detalleActor.value = value.nombre;
                seRenderea.value = true;
            } else{
                seRenderea.value = false;
                actor.value = actorInicial;              
                store.dispatch("accion/limpiaAcciones");
            }
        };
        onMounted(() => {
            store.dispatch("actor/reqActores");
        });

        return {            
            model,
            actor,
            actores,
            cambio,
            seRenderea,
            accion,
            id_responsable,
            detalleActor,
            origen: toRef(props, "origen"),
            reportes: toRef(props, "reportes")
        };
    },
});
</script>