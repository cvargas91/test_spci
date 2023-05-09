<template>
    <div class="q-px-sm">
        <q-card class="tablaAcciones" 
        >
        <div class="row q-pl-lg">
            <div class="col-4">
                <p class="text-subtitle1 q-mb-md">
                    <b>Tipo de Acción</b>
                </p>
                <q-option-group
                    v-model="group"
                    :options="options"
                    class="tablaAcciones"
                    type="toggle"
                    :model-value="group"
                    @update:model-value="generarAcciones"
            />
            </div>
            <q-separator class="text-textoAzul" inset vertical/>
            <div class="col-4 q-pl-lg">
                <p class="text-subtitle1 q-mb-md">
                    <b>Período Acción</b>
                </p>
                <q-select 
                    clearable 
                    filled 
                    v-model="model" 
                    :options="optionsAnio" 
                    label="Período" 
                />                
            </div>
        </div>
        <q-separator class="text-textoAzul" inset horizontal/>
        <q-space></q-space>
        <q-space></q-space>
        <q-space></q-space>
                
        <TablaAcciones
            v-if="!model"
            :acciones="grupoAcciones"
            referencia="AccionesPOA"
        />
        <TablaAcciones
            v-if="model"
            :acciones="generarAccionesPeriodo()"
            referencia="AccionesPOA"
        />

        <q-separator color="blue" inset />
        </q-card>      
    </div>
</template>
<script>
import { ref, toRef, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import TablaAcciones from "src/components/TablaAcciones.vue";

export default defineComponent({
    components: {
        TablaAcciones
    },
    props: {
        acciones: Array,
        referencia: String,
    },
    setup(props) {
        const router = useRouter();
        const store = useStore();
        const accion = computed(() => store.state.accion);
        const acciones = props.acciones;
        const model = ref();
        const filtraPeriodo = (valores) => {
            if (valores)
                return valores.map(elemento => elemento.accion.anio).filter((v, i, a) => a.indexOf(v) === i)
            else
                return [];            
        };   
        
        const opciones = Object.keys(acciones[0]);
        const valores = Object.values(acciones[0]);        
        const optionsAnio = ref(filtraPeriodo(valores[0]));
        const grupoAcciones = ref(valores[0]);


        const options = []
        for (let i=0; i<opciones.length; i++){
            let label = "";            
            switch (opciones[i]) {
                case 'POA':
                    if (valores[i][i].accion.proyecto)                        
                        label = "Acciones URY";
                    else
                        label = "Acciones Transversales";
                break;
                case 'PMI':
                    label = "Acciones PMI";
                break;
                case 'TRANSVERSAL':
                    label = "Acciones Transversales";
                break;
                case 'URY':
                    label = "Acciones URY";
                break;
                //default:
                //    label = "Acciones Transversales";
            }
            options.push({
                "label": label,
                "value": valores[i]
            })
        }
        
        const generarAcciones = (value) =>{
            store.dispatch("accion/limpiaDetalleAccion");
            let acciones = [];
            
            value.forEach(elemento => {
                elemento.forEach(accion => acciones.push(accion))
            });
                
            optionsAnio.value = filtraPeriodo(acciones);
            grupoAcciones.value = acciones;
        };
        const generarAccionesPeriodo = (value) =>{
            store.dispatch("accion/limpiaDetalleAccion");            
            if(model.value){
                return grupoAcciones.value.filter(elemento => elemento.accion.anio == model.value);
            }else{
                return grupoAcciones.value;
            }
            //optionsAnio.value = filtraPeriodo(grupoAcciones.value);
        };
        return {
            options,
            filtraPeriodo,
            generarAcciones,
            generarAccionesPeriodo,
            grupoAcciones,
            //acciones: toRef(props, "acciones"),
            referencia: toRef(props, "referencia"),
            filter: ref(""),
            initialPagination: {
                page: 1,
                rowsPerPage: 5,
            },
            //tab: ref("funciones"),
            splitterModel: ref(15),
            accion,
            group: ref([valores[0]]),
            optionsAnio,
            model,
        };
    },
});
</script>  