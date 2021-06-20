<template>
  <div class="content">
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-size-50"
        v-if="this.role==0||this.role==1  ? true : false"
      >
        <new-store-form data-background-color="orange"></new-store-form>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-size-50"
        v-if="this.role==0||this.role==1 ? true : false"
      >
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">入库</h4>
            <p class="category">从已完成的进货单中入库</p>
          </md-card-header>
          <md-card-content>
            <store-from-import-table data-header-color="green"></store-from-import-table>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item" v-if="this.role==4 ? true : false">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">入库</h4>
            <p class="category">从已完成的进货单中入库</p>
          </md-card-header>
          <md-card-content>
            <store-from-import-table data-header-color="green"></store-from-import-table>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
        v-if="this.role==0||this.role==1 ||this.role==4 ? true : false"
      >
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">库存管理</h4>
            <p class="category">手动管理所有库存商品</p>
          </md-card-header>
          <md-card-content>
            <store-table table-header-color="orange"></store-table>
          </md-card-content>
        </md-card>
      </div>

      <!--<div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100">
        <md-card class="md-card-plain">
          <md-card-header data-background-color="green">
            <h4 class="title">进货管理员</h4>
            <p class="category">Here is a subtitle for this table</p>
          </md-card-header>
          <md-card-content>
            <ordered-table></ordered-table>
          </md-card-content>
        </md-card>
      </div>-->
    </div>
  </div>
</template>

<script>
import { NewStoreForm } from "@/pages";
import { StoreTable } from "@/components";
import { StoreFromImportTable } from "@/components";
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  components: {
    StoreTable,
    NewStoreForm,
    StoreFromImportTable
  },
  data() {
    return {
      role: -1
    };
  },
  mounted() {
    Vue.http.get("/checklogin").then(
      response => {
        this.role = Cookies.get("role");
        if (this.role != "0" && this.role != "1" && this.role != "4") {
          this.$router.replace({
            path: "/login"
          });
        }
      }, //Error callback
      response => {
        if (response.status != 200) {
          this.$router.replace({
            path: "/login"
          });
        }
      }
    );
  }
};
</script>
