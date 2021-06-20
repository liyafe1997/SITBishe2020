<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
        <stats-card data-background-color="blue">
          <template slot="header">
            <md-icon>supervised_user_circle</md-icon>
          </template>

          <template slot="content">
            <p class="category">用户总数</p>
            <h3 class="title">
              {{countdata.UserCount}}
              <small>个</small>
            </h3>
            <small class="category">（总登录 {{countdata.LoginCount}}  次）</small>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>zoom_out_map</md-icon>
              <a href="/user">管理用户...</a>
            </div>
          </template>
        </stats-card>
      </div>
      <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
        <stats-card data-background-color="orange">
          <template slot="header">
            <md-icon>store</md-icon>
          </template>

          <template slot="content">
            <p class="category">库存商品</p>
            <h3 class="title">
              {{countdata.StoreCount}}
              <small>种</small>
            </h3>
            <small class="category">（共 {{countdata.AllStoreCount}} 件商品）</small>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>zoom_out_map</md-icon>
              <a href="/importtable">管理库存...</a>
            </div>
          </template>
        </stats-card>
      </div>
      <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
        <stats-card data-background-color="red">
          <template slot="header">
            <md-icon>today</md-icon>
          </template>

          <template slot="content">
            <p class="category">销售订单</p>
            <h3 class="title">
              {{countdata.SaleCount}}
              <small>张</small>
            </h3>
            <small class="category">（共 {{countdata.AllSaleCount}} 件商品）</small>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>zoom_out_map</md-icon>
              <a href="/saletable">管理销售订单...</a>
            </div>
          </template>
        </stats-card>
      </div>
      <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
        <stats-card data-background-color="green">
          <template slot="header">
            <md-icon>add_shopping_cart</md-icon>
          </template>

          <template slot="content">
            <p class="category">进货订单</p>
            <h3 class="title">
              {{countdata.ImportCount}}
              <small>张</small>
            </h3>
            <small class="category">（共 {{countdata.AllImportCount}} 件商品）</small>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>zoom_out_map</md-icon>
              <a href="/importtable">进货管理...</a>
            </div>
          </template>
        </stats-card>
      </div>
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
        <md-card>
          <md-card-header data-background-color="blue">
            <h4 class="title">登录记录</h4>
            <p class="category">最近5次用户登录记录</p>
          </md-card-header>
          <md-card-content>
            <login-history-ordered-table table-header-color="blue"></login-history-ordered-table>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">库存商品排行</h4>
            <p class="category">库存数量最大Top5商品</p>
          </md-card-header>
          <md-card-content>
            <store-ordered-table table-header-color="orange"></store-ordered-table>
          </md-card-content>
        </md-card>
      </div>

      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
        <md-card>
          <md-card-header data-background-color="red">
            <h4 class="title">销售单排行</h4>
            <p class="category">销售量最大Top5商品</p>
          </md-card-header>
          <md-card-content>
            <sale-ordered-table table-header-color="red"></sale-ordered-table>
          </md-card-content>
        </md-card>
      </div>
      <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">进货单排行</h4>
            <p class="category">进货数量最大Top5商品</p>
          </md-card-header>
          <md-card-content>
            <import-ordered-table table-header-color="green"></import-ordered-table>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import {
  StatsCard,
  SaleOrderedTable,
  StoreOrderedTable,
  ImportOrderedTable,
  LoginHistoryOrderedTable
} from "@/components";
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  components: {
    StatsCard,
    SaleOrderedTable,
    ImportOrderedTable,
    StoreOrderedTable,
    LoginHistoryOrderedTable
  },
  data() {
    return {
      countdata: {}
    };
  },
  mounted() {
    Vue.http.get("/checklogin").then(
      response => {
        this.role = Cookies.get("role");
        if (this.role != "0") {
          this.$router.replace({
            path: "/login",
          });
        }
      }, //Error callback
      response => {
        if (response.status != 200) {
                    this.$router.replace({
            path: "/login",
          });
        }
      }
    );
    this.getData();
  },
  methods: {
    getData() {
      Vue.http.get("/get_dashboard_count").then(response => {
        this.countdata = response.body;
      });
    }
  }
};
</script>
