import {Injectable} from '@angular/core';
import {OrderServiceInterface} from "../../domain/interfaces/services/order-service-interface";
import {Observable} from "rxjs";
import {Order} from "../../domain/entities/order";
import {OrderAdapterService} from "../../../infrastructure/adapters/services/order-adapter.service";

@Injectable({
  providedIn: 'root'
})
export class OrderService implements OrderServiceInterface {

  constructor(private orderAdapter: OrderAdapterService) {
  }

  public sendOrder(order: Order): Observable<void> {
    console.log(order);
    return this.orderAdapter.sendOrder(order);
  }
}
