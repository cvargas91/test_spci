
<template>    
    <q-table
        :rows="reportes"
        :columns="opciones"
        :selection="opcion"
        row-key="id"
        v-model:selected="accionesSeleccionadas"
        @update:selected="emitirSeleccion()"
        no-data-label="No hay acciones para el filtro aplicado"
        :filter="filter"
        class="tablaAcciones"
    >
        <template v-slot:top-right>
            <q-input borderless dense debounce="300" v-model="filter" placeholder="Filtrar">
                <template v-slot:append>
                    <q-icon name="search" />
                </template>
            </q-input>
        </template>
        <!--<template v-slot:header-cell-checkBox="props">
            <q-checkbox v-model="props.accionesSeleccionadas" />
        </template>-->
    
        <template v-slot:body-cell-checkBox="props">
            <q-checkbox :model-value="props.accionesSeleccionadas" @update:model-value="(val, evt) => { val }" />
        </template>

        <template v-slot:body-cell-infoButton="props">
            <q-tr :props="props" style="height:55px;">
                <q-td auto-width>
                    <q-btn 
                        size="sm" 
                        color="btnCancelar" 
                        round dense 
                        @click="toggleExpandAndFilter(props)"
                        :icon="props.expand ? 'remove' : 'add'"
                    />
                    <!--@click="props.expand = !props.expand" :icon="props.expand ? 'remove' : 'add'"-->
                </q-td>
                <q-td
                    v-for="col in props.cols"
                    :key="col.name"
                    :props="props"                    
                >
                    {{ col.value }}
                </q-td>
            </q-tr>
            <q-tr v-show="props.expand" :props="props">
                
                <q-td colspan="100%">
                    <div class="text-left">Acciones en Reporte N°{{ props.row.id }}: 
                        <!--<li v-for="(item, id) in props.row.reporte_acciones" :key="id">{{ item.accion }}</li>-->
                        <li v-for="(item, id) in idUaysenAcciones" :key="id">{{ item }}</li>
                    </div>
                </q-td>
            </q-tr>
        </template>
    </q-table>
</template>

<script>
import { ref, toRef,computed, onMounted, onUnmounted, defineComponent } from "vue";
import { useStore } from "vuex";

export default defineComponent({
    props: {
        reportes: Array,
        reporteSeleccionado: Object,
        opcion: Boolean,
    },
    methods: {
        async emitirSeleccion() {                
            await this.$emit("cambio-seleccion", this.accionesSeleccionadas);            
        },
        toggleExpandAndFilter(props) {
            props.expand = !props.expand;
            if(props.expand){
                this.filtrarAcciones(props.row.reporte_acciones);
            }            
        },
        filtrarAcciones(reporteAcciones) {        
            this.idUaysenAcciones = reporteAcciones.map(accion => {
                const idUaysenIncluidos = this.accion.acciones.find(elemento => elemento.accion.id === accion.accion);
                return idUaysenIncluidos ? idUaysenIncluidos.accion.id_uaysen : null;
            });     
        }
    },
    watch: {
        reporteSeleccionado(nuevoValor){
            this.accionesSeleccionadas = nuevoValor;
        },
    },
    setup(props) {
        const store = useStore();    
        const accion = computed(() => store.state.accion);
        const idUaysenAcciones = ref([]);
        const opcion = ref("");
        const reportes = computed({
            get:() => props.reportes
        });
        const seRenderea = ref(false);
        const actores = computed(() => store.state.actor.actores);
        const accionesSeleccionadas = ref([]);

        const reporteSeleccionado = computed({
            get: () => props.reporteSeleccionado
        });

        const getValor = (actor) => {
            let detalleActor = actores.value.filter(elemento => elemento.id === actor).map(detalle => detalle.id_uaysen);
            return (detalleActor[0]);
        };
        if(props.reportes.length){
            if(props.reportes[0].estado === "Finalizado"){
                seRenderea.value = true;
            }
        }    

        if(props.opcion){
            opcion.value = "single"
        }else{
            opcion.value = "none"
        }

        return {
            opcion,
            accion,
            idUaysenAcciones,
            reportes,
            seRenderea,
            getValor,
            accionesSeleccionadas,
            reporteSeleccionado,            
            opciones: [
                { name: 'infoButton', field: 'infoButton', align: 'left', sortable: false, label: 'Ver Acciones' },
                {
                    name: "reporte",
                    label: "N° Reporte",
                    field: "id",
                    align: "left",
                },
                {
                    name: "unidad",
                    label: "Unidad",
                    field: (row) => (getValor(row.actor)),
                    align: "left",
                    sortable: true,
                },
                {
                    name: "creado",
                    label: "Creado",
                    field: "creado",
                    align: "left",
                    sortable: true,
                },
                {
                    name: "creado",
                    label: "Modificado",                    
                    field: "modificado",
                    align: "left",
                    sortable: true,
                },
                {
                    name: "enviado",
                    label: "Enviado",
                    field: (row) => {
                        if(row.enviado)
                            return "Enviado a " + getValor(row.actor);
                        else
                            return "-"
                    },
                    align: "left",
                    sortable: true,
                }
            ]

        }
    }

})
</script>
    