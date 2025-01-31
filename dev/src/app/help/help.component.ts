import { Component, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { SidebarModule } from 'primeng/sidebar';

@Component({
  selector: 'app-help',
  imports: [MatIconModule, SidebarModule, MatButtonModule],
  templateUrl: './help.component.html',
  styleUrl: './help.component.scss'
})
export class HelpComponent {
  helpVisible = signal<boolean>(false);

  toggleHelp(): void {
    this.helpVisible.set(!this.helpVisible());
  }
}
