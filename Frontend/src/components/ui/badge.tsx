import React, { forwardRef } from "react";
import { Badge as BootstrapBadge } from "react-bootstrap";
import { cn } from "../../lib/utils";

export interface BadgeProps
  extends React.ComponentPropsWithoutRef<typeof BootstrapBadge> {
  variant?:
    | "primary"
    | "secondary"
    | "success"
    | "danger"
    | "warning"
    | "info"
    | "light"
    | "dark";
  className?: string;
  children?: React.ReactNode;
}

const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  ({ variant = "primary", className, children, ...props }, ref) => {
    return (
      <BootstrapBadge
        ref={ref}
        bg={variant}
        className={cn(
          "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
          className
        )}
        {...props}
      >
        {children}
      </BootstrapBadge>
    );
  }
);
Badge.displayName = "Badge";

export { Badge };
