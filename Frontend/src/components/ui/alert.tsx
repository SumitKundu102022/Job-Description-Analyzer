import React, { forwardRef } from "react";
import { Alert as BootstrapAlert } from "react-bootstrap";
import { AlertCircle } from "lucide-react";
import { cn } from "../../lib/utils";

export interface AlertProps
  extends React.ComponentPropsWithoutRef<typeof BootstrapAlert> {
  variant?: "default" | "destructive";
  className?: string;
  children?: React.ReactNode;
  title?: string; // Added title prop
}

const Alert = forwardRef<HTMLDivElement, AlertProps>(
  ({ variant = "default", className, children, title, ...props }, ref) => {
    let bsVariant = "primary"; // Default Bootstrap variant
    if (variant === "destructive") {
      bsVariant = "danger";
    }

    return (
      <BootstrapAlert
        ref={ref}
        variant={bsVariant}
        className={cn("relative w-full rounded-md border p-4", className)}
        {...props}
      >
        {title && <h4 className="alert-heading">{title}</h4>}
        {children}
      </BootstrapAlert>
    );
  }
);
Alert.displayName = "Alert";

const AlertTitle = ({
  className,
  children,
  ...props
}: {
  className?: string;
  children?: React.ReactNode;
}) => (
  <div className={cn("text-lg font-semibold", className)} {...props}>
    {children}
  </div>
);

const AlertDescription = ({
  className,
  children,
  ...props
}: {
  className?: string;
  children?: React.ReactNode;
}) => (
  <div className={cn("text-sm", className)} {...props}>
    {children}
  </div>
);

export { Alert, AlertTitle, AlertDescription };
