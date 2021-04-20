<template>
  <div class="manage_alerts">
    <h1>Manage alerts</h1>
  </div>
  <div class="card">
    <DataTable :value="products"
               responsiveLayout="scroll"
               :paginator="true"
               :rows="5"
               paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
               :rowsPerPageOptions="[5,10,50]"
               currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
               sortField="name"
               :sortOrder="1"
               removableSort
               :globalFilterFields="['name','code','category','quantity']"
               v-model:filters="filters1"
               filterDisplay="menu"
               v-model:selection="selectedProducts3"
               dataKey="code"
               v-model:expandedRows="expandedRows"
               ref="dt"
               :resizableColumns="true"
               columnResizeMode="fit">

      <template #header style="width: fit-content">
        <div style="display: grid;
        grid-template-columns: repeat(6, 1fr);
          grid-template-rows: repeat(2, 1fr);
          grid-column-gap: 0;
          grid-row-gap: 0;
width: fit-content;">
          <Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" style="width: 30%;grid-area:  1 / 1 / 2 / 2;"/>
          <MultiSelect :modelValue="selectedColumns"
                     :options="columns"
                     optionLabel="header"
                     @update:modelValue="onToggle"
                     placeholder="Select Columns"
                     style="width: 75%; grid-area:  2 / 1 / 3 / 2;"/>
          <Button icon="pi pi-plus" label="Expand All" @click="expandAll" class="p-mr-2" style="width: 100%;grid-area:  1 / 3 / 2 / 4;"/>
          <Button icon="pi pi-minus" label="Collapse All" @click="collapseAll" style="width: 100%;grid-area:  1 / 4 / 2 / 5;"/>
          <Button type="button" icon="pi pi-filter-slash"
                  label="Clear" class="p-button-outlined"
                  @click="clearFilter1()"
                  style="grid-area: 1 / 6 / 2 / 7;"/>
          <span class="p-input-icon-left" style="grid-area: 2 / 6 / 3 / 7;">
              <i class="pi pi-search"/>
              <InputText v-model="filters1['global'].value" placeholder="Keyword Search"/>
          </span>
          </div>
      </template>

      <Column id="alert-expand" :expander="true" headerStyle="width: 3rem" />
      <Column id="alert-select" selectionMode="multiple" headerStyle="width: 3em" />
      <Column v-for="(col, index) of selectedColumns" :field="col.field" :header="col.header" :key="col.field + '_' + index" :sortable="true"/>
      <template #expansion="slotProps">
        <h5>Details about {{ slotProps.data.name }}</h5>
      </template>

    </DataTable>
  </div>
</template>

<script>
import {FilterMatchMode, FilterOperator} from 'primevue/api';

export default {
  data() {
    return {
      columns: [
        {field: 'code', header: 'Code'},
        {field: 'name', header: 'Name'},
        {field: 'category', header: 'Category'},
        {field: 'quantity', header: 'Quantity'}
      ],
      products: [
        {
          "id": "1000",
          "code": "f230fh0g3",
          "name": "Bamboo Watch",
          "description": "Product Description",
          "image": "bamboo-watch.jpg",
          "price": 65,
          "category": "Accessories",
          "quantity": 24,
          "inventoryStatus": "INSTOCK",
          "rating": 5
        },
        {
          "id": "1001",
          "code": "nvklal433",
          "name": "Black Watch",
          "description": "Product Description",
          "image": "black-watch.jpg",
          "price": 72,
          "category": "Accessories",
          "quantity": 61,
          "inventoryStatus": "INSTOCK",
          "rating": 4
        },
        {
          "id": "1002",
          "code": "zz21cz3c1",
          "name": "Blue Band",
          "description": "Product Description",
          "image": "blue-band.jpg",
          "price": 79,
          "category": "Fitness",
          "quantity": 2,
          "inventoryStatus": "LOWSTOCK",
          "rating": 3
        },
        {
          "id": "1003",
          "code": "244wgerg2",
          "name": "Blue T-Shirt",
          "description": "Product Description",
          "image": "blue-t-shirt.jpg",
          "price": 29,
          "category": "Clothing",
          "quantity": 25,
          "inventoryStatus": "INSTOCK",
          "rating": 5
        },
        {
          "id": "1004",
          "code": "h456wer53",
          "name": "Bracelet",
          "description": "Product Description",
          "image": "bracelet.jpg",
          "price": 15,
          "category": "Accessories",
          "quantity": 73,
          "inventoryStatus": "INSTOCK",
          "rating": 4
        },
        {
          "id": "1005",
          "code": "av2231fwg",
          "name": "Brown Purse",
          "description": "Product Description",
          "image": "brown-purse.jpg",
          "price": 120,
          "category": "Accessories",
          "quantity": 0,
          "inventoryStatus": "OUTOFSTOCK",
          "rating": 4
        },
        {
          "id": "1006",
          "code": "bib36pfvm",
          "name": "Chakra Bracelet",
          "description": "Product Description",
          "image": "chakra-bracelet.jpg",
          "price": 32,
          "category": "Accessories",
          "quantity": 5,
          "inventoryStatus": "LOWSTOCK",
          "rating": 3
        },
        {
          "id": "1007",
          "code": "mbvjkgip5",
          "name": "Galaxy Earrings",
          "description": "Product Description",
          "image": "galaxy-earrings.jpg",
          "price": 34,
          "category": "Accessories",
          "quantity": 23,
          "inventoryStatus": "INSTOCK",
          "rating": 5
        },
        {
          "id": "1008",
          "code": "vbb124btr",
          "name": "Game Controller",
          "description": "Product Description",
          "image": "game-controller.jpg",
          "price": 99,
          "category": "Electronics",
          "quantity": 2,
          "inventoryStatus": "LOWSTOCK",
          "rating": 4
        },
        {
          "id": "1009",
          "code": "cm230f032",
          "name": "Gaming Set",
          "description": "Product Description",
          "image": "gaming-set.jpg",
          "price": 299,
          "category": "Electronics",
          "quantity": 63,
          "inventoryStatus": "INSTOCK",
          "rating": 3
        }
      ],
      selectedColumns: null,
      selectedProducts3: null,
      filters1: null,
      expandedRows: []
    }
  },
  created() {
    this.initFilters1();
    this.selectedColumns = this.columns;
  },
  methods: {
    clearFilter1() {
      this.initFilters1();
    },
    initFilters1() {
      this.filters1 = {
        'global': {value: null, matchMode: FilterMatchMode.CONTAINS},
        'name': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
        'code': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]},
        'category': {value: null, matchMode: FilterMatchMode.IN},
        'quantity': {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.DATE_IS}]},
      }
    },
    expandAll() {
      this.expandedRows = this.products.filter(p => p.id);
    },
    collapseAll() {
      this.expandedRows = null;
    },
    onToggle(value) {
      this.selectedColumns = this.columns.filter(col => value.includes(col));
    },
    exportCSV() {
      this.$refs.dt.exportCSV();
    }
  }
}
</script>