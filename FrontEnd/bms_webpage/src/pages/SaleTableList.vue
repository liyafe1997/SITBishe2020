<template>
  <div class="content">
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-100 md-size-50"
        v-if="this.role==0||this.role==3  ? true : false"
      >
        <new-sale-form data-background-color="red"></new-sale-form>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-size-50"
        v-if="this.role==0||this.role==3 ? true : false"
      >
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">新销售</h4>
            <p class="category">从库存中销售商品</p>
          </md-card-header>
          <md-card-content>
            <sale-from-store-table data-header-color="green"></sale-from-store-table>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item" v-if="this.role==5 ? true : false">
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">新销售</h4>
            <p class="category">从库存中销售商品</p>
          </md-card-header>
          <md-card-content>
            <sale-from-store-table data-header-color="green"></sale-from-store-table>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100"
        v-if="this.role==0||this.role==3||this.role==5 ? true : false"
      >
        <md-card>
          <md-card-header data-background-color="red">
            <h4 class="title">销售单管理</h4>
            <p class="category" v-if="this.role==5 ? false :true ">手动管理销售单</p>
          </md-card-header>
          <md-card-content>
            <sale-table table-header-color="red"></sale-table>
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
import { NewSaleForm } from "@/pages";
import { SaleTable } from "@/components";
import { SaleFromStoreTable } from "@/components";
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  components: {
    SaleTable,
    NewSaleForm,
    SaleFromStoreTable
  },
  data() {
    return { role: -1 };
  },
  mounted() {
    Vue.http.get("/checklogin").then(
      response => {
        this.role = Cookies.get("role");
        if (this.role != "0" && this.role != "3" && this.role != "5") {
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
