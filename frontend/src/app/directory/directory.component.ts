import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { NzMessageService } from 'ng-zorro-antd';
import { Router, ActivatedRoute, ParamMap, NavigationEnd } from '@angular/router';

import { switchMap } from 'rxjs/operators';

const fakeDataUrl = '/api/';

@Component({
  selector: 'app-directory',
  templateUrl: './directory.component.html',
  styleUrls: ['./directory.component.css']
})
export class DirectoryComponent implements OnInit {

  loading = true; // bug
  loadingMore = false;
  showLoadingMore = true;
  data = [];

  pathBase = '/'

  constructor(
    private http: HttpClient,
    private msg: NzMessageService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.jumpTo('');
  }

  jumpTo(path: string) {
    this.pathBase = (this.pathBase + path).split('/').filter(s => s).join('/') + '/';
    this.getData(this.pathBase, (res: any) => {
      this.data = res['data']['name_list'].filter(e => e[1][0] != '.');
      console.log(res);
      this.loading = false;
    })
  }

  getData(path: string, callback: (res: any) => void) {
    if (!path) {
      path = '';
    }
    return this.http.get(fakeDataUrl + path).subscribe((res: any) => callback(res));
  }

  onLoadMore(): void {
    this.loadingMore = true;
    this.http.get(fakeDataUrl).subscribe((res: any) => {
      this.data = this.data.concat(res.results);
      this.loadingMore = false;
    });
  }

  edit(item: any): void {
    this.msg.success(item.email);
  }
}
